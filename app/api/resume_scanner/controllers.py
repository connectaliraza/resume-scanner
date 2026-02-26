import os
import shutil

from fastapi import File, UploadFile

from app.api.base_components import BaseController, Endpoint, Response
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

    async def upload(self, file: UploadFile = File(...)) -> Response:
        file_path = os.path.join(MEDIA_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return self.service.upload_resume(
            filename=file.filename, content_type=file.content_type, file_path=file_path
        )

    async def parse(self, resume_id: int) -> Response:
        resume = self.service._resume_repository._db.get_by_id("resumes", resume_id)
        if not resume:
            return Response(
                status_code=404,
                message="Resume not found",
                error_code=2004,
            )

        file_path = os.path.join(MEDIA_PATH, resume["filename"])
        if not os.path.exists(file_path):
            return Response(
                status_code=404,
                message="Resume file not found",
                error_code=2005,
            )

        return self.service.parse_resume(
            resume_id=resume_id,
            file_path=file_path,
            content_type=resume["content_type"],
        )
