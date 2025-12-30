from pathlib import Path
from uuid import UUID, uuid4
from fastapi import UploadFile, HTTPException
import aiofiles
import os

async def save_uploaded_file(user_id: UUID, file: UploadFile, upload_dir: str = "uploads") -> dict:
    """
    Save uploaded file to disk and return file metadata.

    Args:
        user_id: UUID of the user uploading the file
        file: UploadFile object from FastAPI
        upload_dir: Base directory for uploads (default: "uploads")

    Returns:
        dict with file_path, original_filename, file_size, mime_type
    """
    # Create user-specific directory
    user_dir = Path(upload_dir) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = user_dir / unique_filename

    # Save file in chunks
    try:
        file_size = 0
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                await f.write(chunk)
                file_size += len(chunk)

        # Return relative path (from backend directory)
        relative_path = str(file_path)

        return {
            "file_path": relative_path,
            "original_filename": file.filename,
            "file_size": file_size,
            "mime_type": file.content_type
        }
    except Exception as e:
        # Clean up partial file if upload failed
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


def delete_file(file_path: str) -> bool:
    """
    Delete file from filesystem.

    Args:
        file_path: Relative path to the file

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            path.unlink()
            return True
        return False
    except Exception:
        return False


def get_file_path(file_path: str) -> Path:
    """
    Get absolute path to file with security validation.

    Args:
        file_path: Relative path to the file

    Returns:
        Absolute Path object

    Raises:
        HTTPException if path is invalid or outside allowed directory
    """
    try:
        base_dir = Path.cwd()
        full_path = (base_dir / file_path).resolve()

        # Prevent path traversal attacks
        if not str(full_path).startswith(str(base_dir)):
            raise HTTPException(status_code=400, detail="Invalid file path")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return full_path
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file path: {str(e)}")
