from fastapi import File, UploadFile

from app.api.base_components import BaseController, Endpoint
from app.api.resume_scanner.models import ParsedResume, Resume
from app.api.resume_scanner.services import ResumeScannerService


class ResumeScannerController(BaseController):
    def __init__(self, service: ResumeScannerService, api_version: str):
        self.service = service
        self.api_version = api_version

        endpoints = [
            Endpoint(
                rule="/upload",
                func=self.upload,
                methods=["POST"],
                response_type=Resume,
            ),
            Endpoint(
                rule="/{resume_id}/parse",
                func=self.parse,
                methods=["POST"],
                response_type=ParsedResume,
            ),
        ]

        super().__init__(
            title="Resume Scanner",
            prefix=f"/{self.api_version}/resumes",
            endpoints=endpoints,
        )

    async def upload(self, file: UploadFile = File(...)):
        # In a real app, you would save the file to a storage service
        uploaded_resume = self.service.upload_resume(
            filename=file.filename,
            content_type=file.content_type,
        )
        return uploaded_resume

    async def parse(self, resume_id: int):
        parsed_resume = self.service.parse_resume(resume_id=resume_id)
        return parsed_resume
