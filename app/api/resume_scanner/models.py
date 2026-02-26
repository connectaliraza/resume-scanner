from typing import List, Optional

from pydantic import BaseModel


class Resume(BaseModel):
    id: int
    filename: str
    content_type: str


class ParsedResume(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str] = []
    education: List[dict] = []
    experience: List[dict] = []
    certifications: List[dict] = []
    projects: List[dict] = []
