from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..models import Document
from ..schemas import DocumentUpdate, DocumentResponse
from ..services import file_storage

router = APIRouter(prefix="/documents", tags=["documents"])

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: UUID, document_update: DocumentUpdate, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    update_data = document_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)
    return document

@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete physical file from storage
    file_storage.delete_file(document.file_path)

    # Delete database record
    db.delete(document)
    db.commit()
    return None

@router.get("/{document_id}/download")
def download_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get file path and verify it exists
    file_path = file_storage.get_file_path(document.file_path)

    return FileResponse(
        path=file_path,
        filename=document.original_filename,
        media_type=document.mime_type or "application/pdf",
        headers={"Content-Disposition": f"attachment; filename={document.original_filename}"}
    )

@router.get("/{document_id}/view")
def view_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get file path and verify it exists
    file_path = file_storage.get_file_path(document.file_path)

    return FileResponse(
        path=file_path,
        media_type=document.mime_type or "application/pdf",
        headers={"Content-Disposition": "inline"}
    )
