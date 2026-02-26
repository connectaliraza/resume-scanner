"""
This module provides utilities for extracting text from different file formats.
"""
import docx
import PyPDF2


def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join([page.extract_text() for page in reader.pages])


def extract_text_from_txt(file_path: str) -> str:
    """Extracts text from a TXT file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
