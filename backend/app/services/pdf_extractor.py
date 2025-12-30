from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file_path: Path to the PDF file (relative or absolute)

    Returns:
        Extracted text as a string

    Raises:
        Exception if PDF extraction fails
    """
    try:
        # Convert to Path object for handling
        path = Path(file_path)

        # Read PDF and extract text from all pages
        reader = PdfReader(str(path))
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        # Concatenate all page texts with newline separators
        full_text = "\n\n".join(text_parts)

        return full_text.strip()

    except Exception as e:
        # Return error message instead of raising exception
        # This allows the document to be saved even if extraction fails
        return f"[PDF text extraction failed: {str(e)}]"
