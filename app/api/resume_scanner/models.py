from typing import List, Optional

from pydantic import BaseModel, Field


class Resume(BaseModel):
    id: int
    filename: str
    content_type: str


class ParsedResume(BaseModel):
    full_name: Optional[str] = Field(None, alias="Full Name")
    email: Optional[str] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    skills: List[str] = Field([], alias="Skills")
    education: List[dict] = Field([], alias="Education")
    experience: List[dict] = Field([], alias="Work Experience")
    certifications: List[dict] = Field([], alias="Certifications")
    projects: List[dict] = Field([], alias="Projects")

    class Config:
        populate_by_name = True
