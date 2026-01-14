from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from ..database import get_db, SessionLocal
from ..models import User, Document
from ..schemas import DocumentCreate, DocumentResponse, StatsResponse
from ..services import file_storage, pdf_extractor
from ..services.ai import get_embedding
from ..config import settings

router = APIRouter(prefix="/users", tags=["users"])


async def generate_document_embedding(document_id: str, content: str):
    """Background task to generate and store document embedding"""
    try:
        print(f"[Embedding] Starting embedding generation for document {document_id}")
        print(f"[Embedding] Content length: {len(content)} chars")

        # Generate embedding using Cohere API
        embedding = await get_embedding(content[:8000])
        print(f"[Embedding] Generated embedding with {len(embedding)} dimensions")

        # Convert embedding list to PostgreSQL vector format: [0.1,0.2,0.3]
        # pgvector expects a string like "[0.1,0.2,0.3]" without spaces
        embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
        print(f"[Embedding] Formatted embedding string (first 100 chars): {embedding_str[:100]}...")

        # Store embedding in database
        db = SessionLocal()
        try:
            print(f"[Embedding] Updating database for document {document_id}")
            result = db.execute(
                text("""
                    UPDATE documents
                    SET embedding = :embedding::vector
                    WHERE id = :document_id::uuid
                """),
                {
                    "embedding": embedding_str,
                    "document_id": document_id
                }
            )
            db.commit()
            print(f"[Embedding] Database update affected {result.rowcount} rows")

            # Verify the update
            verify_result = db.execute(
                text("SELECT embedding IS NOT NULL as has_embedding FROM documents WHERE id = :document_id::uuid"),
                {"document_id": document_id}
            ).first()

            if verify_result and verify_result[0]:
                print(f"[Embedding] ✓ Successfully stored embedding for document {document_id}")
            else:
                print(f"[Embedding] ✗ Warning: Embedding is still NULL after update for document {document_id}")

        except Exception as db_error:
            print(f"[Embedding] Database error: {type(db_error).__name__}: {db_error}")
            raise
        finally:
            db.close()

    except Exception as e:
        print(f"[Embedding] Failed to generate embedding for document {document_id}: {type(e).__name__}: {e}")
        import traceback
        print(f"[Embedding] Traceback: {traceback.format_exc()}")


@router.get("/{user_id}/documents", response_model=List[DocumentResponse])
def get_user_documents(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    documents = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()
    return documents

@router.post("/{user_id}/documents", response_model=DocumentResponse, status_code=201)
async def upload_document(
    user_id: UUID,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Validate file size (check against configured max)
    file_size = 0
    temp_content = await file.read()
    file_size = len(temp_content)

    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size / (1024 * 1024)}MB"
        )

    # Reset file pointer for saving
    await file.seek(0)

    # Save file to storage
    try:
        file_metadata = await file_storage.save_uploaded_file(
            user_id=user_id,
            file=file,
            upload_dir=settings.upload_dir
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract text from PDF
    try:
        extracted_text = pdf_extractor.extract_text_from_pdf(file_metadata["file_path"])
    except Exception as e:
        # If extraction fails, set a default message
        extracted_text = f"[Text extraction failed: {str(e)}]"

    # Create document record in database
    new_document = Document(
        user_id=user_id,
        file_path=file_metadata["file_path"],
        original_filename=file_metadata["original_filename"],
        file_size=file_metadata["file_size"],
        mime_type=file_metadata["mime_type"],
        title=title,
        content=extracted_text,
        status="processed"  # Set to processed after successful extraction
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    # Generate embedding in background (non-blocking)
    background_tasks.add_task(
        generate_document_embedding,
        document_id=str(new_document.id),
        content=extracted_text
    )

    return new_document

@router.get("/{user_id}/stats", response_model=StatsResponse)
def get_user_stats(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_documents = db.query(Document).filter(Document.user_id == user_id).count()

    status_counts = db.query(
        Document.status, func.count(Document.id)
    ).filter(Document.user_id == user_id).group_by(Document.status).all()

    documents_by_status = {status: count for status, count in status_counts}

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_documents_count = db.query(Document).filter(
        Document.user_id == user_id,
        Document.created_at >= seven_days_ago
    ).count()

    return StatsResponse(
        total_documents=total_documents,
        documents_by_status=documents_by_status,
        recent_documents_count=recent_documents_count
    )
