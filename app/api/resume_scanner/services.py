from app.api.resume_scanner.repositories import ResumeRepository
from app.utils.file_extractor import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_txt,
)
from app.utils.llm_extractor import extract_with_llm


class ResumeScannerService:
    def __init__(self, resume_repository: ResumeRepository):
        self._resume_repository = resume_repository

    def upload_resume(self, filename: str, content_type: str, file_path: str) -> dict:
        # In a real app, you would save the file to a storage service
        return self._resume_repository.create_resume(filename, content_type)

    def parse_resume(self, resume_id: int, file_path: str, content_type: str) -> dict:
        try:
            docx_type = (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
            if content_type == "application/pdf":
                text = extract_text_from_pdf(file_path)
            elif content_type == docx_type:
                text = extract_text_from_docx(file_path)
            elif content_type == "text/plain":
                text = extract_text_from_txt(file_path)
            else:
                raise ValueError("Unsupported file type")

            # Attempt to parse with LLM
            parsed_data = extract_with_llm(text)

            # In a real app, you would have more robust validation and error handling
            if not parsed_data:
                raise ValueError("Failed to parse resume with LLM")

            return self._resume_repository.create_parsed_resume(resume_id, parsed_data)

        except Exception as e:
            # Fallback to saving partial data or logging the error
            print(f"Error parsing resume: {e}")
            # For now, we'll just return an empty dictionary
            return {}
