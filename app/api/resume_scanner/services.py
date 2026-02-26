_resumes_db = {}
_parsed_resumes_db = {}


class ResumeScannerService:
    def upload_resume(self, filename: str, content_type: str) -> dict:
        resume_id = len(_resumes_db) + 1
        _resumes_db[resume_id] = {
            "id": resume_id,
            "filename": filename,
            "content_type": content_type,
        }
        return _resumes_db[resume_id]

    def parse_resume(self, resume_id: int) -> dict:
        # In a real app, you would parse the resume content here
        parsed_data = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "skills": ["Python", "FastAPI", "Pydantic"],
        }
        _parsed_resumes_db[resume_id] = parsed_data
        return parsed_data
