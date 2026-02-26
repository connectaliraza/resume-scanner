from app.api.resume_scanner.models import ParsedResume, Resume
from app.db.database import Database


class ResumeRepository:
    def __init__(self, db: Database):
        self._db = db

    def create_resume(self, filename: str, content_type: str) -> Resume:
        resume_data = {"filename": filename, "content_type": content_type}
        created_resume = self._db.add("resumes", resume_data)
        return Resume(**created_resume)

    def create_parsed_resume(self, resume_id: int, parsed_data: dict) -> ParsedResume:
        parsed_resume_data = {"resume_id": resume_id, **parsed_data}
        created_parsed_resume = self._db.add("parsed_resumes", parsed_resume_data)
        return ParsedResume(**created_parsed_resume)
