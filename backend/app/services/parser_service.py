from pathlib import Path

import pymupdf
from docx import Document


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    document = pymupdf.open(file_path)

    try:
        pages = [page.get_text() for page in document]
        return "\n".join(pages).strip()
    finally:
        document.close()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    return "\n".join(paragraphs).strip()


def extract_resume_text(file_path: str) -> str:
    """Extract text from a supported resume file."""
    extension = Path(file_path).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Only PDF and DOCX are supported."
        )

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_docx(file_path)