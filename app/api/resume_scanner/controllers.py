import os
import shutil

from fastapi import File, HTTPException, UploadFile, status

from app.api.base_components import BaseController, Endpoint
from app.api.resume_scanner.models import ParsedResume, Resume
from app.api.resume_scanner.services import ResumeScannerService

MEDIA_PATH = "/home/ubuntu/resume-scanner/media"


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
        file_path = os.path.join(MEDIA_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_resume = self.service.upload_resume(
            filename=file.filename, content_type=file.content_type, file_path=file_path
        )
        return uploaded_resume

    async def parse(self, resume_id: int):
        # In a real app, you would retrieve the file path from the database
        # For now, we'll assume the file exists in the media directory
        resume = self._get_resume_from_db(
            resume_id
        )  # This function needs to be implemented
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
            )

        file_path = os.path.join(MEDIA_PATH, resume.filename)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found"
            )

        parsed_resume = self.service.parse_resume(
            resume_id=resume_id, file_path=file_path, content_type=resume.content_type
        )
        if not parsed_resume:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to parse resume",
            )
        return parsed_resume

    def _get_resume_from_db(self, resume_id: int):
        # This is a placeholder for fetching resume details from the database
        # In a real implementation, this would query the ResumeRepository
        # For now, we'll access the service's repository directly for simplicity
        return self.service._resume_repository._db.get_by_id("resumes", resume_id)
