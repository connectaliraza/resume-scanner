from app.api.base_components import Response
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

    def upload_resume(
        self, filename: str, content_type: str, file_path: str
    ) -> Response:
        resume = self._resume_repository.create_resume(filename, content_type)
        return Response(
            message="Resume uploaded successfully",
            body=resume,
        )

    def parse_resume(
        self, resume_id: int, file_path: str, content_type: str
    ) -> Response:
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
                return Response(
                    status_code=400,
                    message="Unsupported file type",
                    error_code=2001,
                )

            parsed_data = extract_with_llm(text)

            if not parsed_data:
                return Response(
                    status_code=500,
                    message="Failed to parse resume with LLM",
                    error_code=2002,
                )

            parsed_resume = self._resume_repository.create_parsed_resume(
                resume_id, parsed_data
            )
            return Response(
                message="Resume parsed successfully",
                body=parsed_resume,
            )

        except Exception as e:
            return Response(
                status_code=500,
                message=f"Error parsing resume: {e}",
                error_code=2003,
            )
