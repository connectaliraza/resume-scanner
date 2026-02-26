"""
This module provides utilities for extracting text from different file formats.
"""
import docx
import pdfplumber


def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_txt(file_path: str) -> str:
    """Extracts text from a TXT file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
