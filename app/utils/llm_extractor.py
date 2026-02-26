"""
This module provides utilities for extracting structured data from resume text
using Google Gemini.
"""
import json
import os

import google.generativeai as genai

from app.utils.data_transformer import (
    transform_skills_to_list,
    transform_to_list_of_dicts,
)


def _normalize_keys(data: dict) -> dict:
    """Converts dictionary keys from title/space case to snake_case."""
    normalized_data = {}
    for key, value in data.items():
        normalized_key = key.lower().replace(" ", "_")
        normalized_data[normalized_key] = value
    return normalized_data


def extract_with_llm(resume_text: str) -> dict:
    """Extracts structured data from resume text using Google Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""Extract the following information from the resume text below:

- Full Name
- Contact Information (Email, Phone)
- Skills
- Education
- Work Experience
- Certifications
- Projects

Resume Text:
{resume_text}

Return the extracted information in a clean JSON format.
Do not include any extra text or markdown formatting like ```json or ```.
"""

    try:
        response = model.generate_content(prompt)
        parsed_json = json.loads(response.text)
        normalized_data = _normalize_keys(parsed_json)

        # Transform fields to their expected data types
        if "skills" in normalized_data:
            normalized_data["skills"] = transform_skills_to_list(
                normalized_data["skills"]
            )
        if "projects" in normalized_data:
            normalized_data["projects"] = transform_to_list_of_dicts(
                normalized_data["projects"]
            )
        if "education" in normalized_data:
            normalized_data["education"] = transform_to_list_of_dicts(
                normalized_data["education"]
            )
        if "work_experience" in normalized_data:
            normalized_data["work_experience"] = transform_to_list_of_dicts(
                normalized_data["work_experience"]
            )
        if "certifications" in normalized_data:
            normalized_data["certifications"] = transform_to_list_of_dicts(
                normalized_data["certifications"]
            )

        return normalized_data
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error during Gemini extraction or JSON parsing: {e}")
        return {}
