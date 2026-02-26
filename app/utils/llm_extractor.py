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

    prompt = f"""**Resume Parsing Instructions**

**Objective:** Extract structured information from the provided resume
text and return it in a clean JSON format.

**Resume Text:**
```
{resume_text}
```

**Extraction Fields:**

1. **Full Name:**
   - Extract the full name of the candidate.
   - Example: "John Doe"

2. **Contact Information:**
   - **Email:** Extract the primary email address. Look for email
     patterns like name@domain.com
   - **Phone:** Extract the primary phone number. Look for phone
     patterns with digits and common separators.

3. **Skills:**
   - Extract all technical and soft skills mentioned.
   - Return as a flat list of strings.
   - Example: ["Python", "FastAPI", "Teamwork"]

4. **Education:**
   - Extract all educational qualifications.
   - Return as a list of dictionaries.
   - Keys: degree, institution, year.
   - Example: [{{"degree": "Bachelor of Science", "institution":
     "University", "year": "2020"}}]

5. **Work Experience:**
   - Extract all work experience entries.
   - Return as a list of dictionaries.
   - Keys: job_title, company, duration, responsibilities.
   - responsibilities should be a list of strings.
   - Example: [{{"job_title": "Software Engineer", "company":
     "Tech Corp", "duration": "2020-2022", "responsibilities":
     ["Developed features", "Fixed bugs"]}}]

6. **Certifications:**
   - Extract all certifications and licenses.
   - Return as a list of dictionaries.
   - Keys: name, issuing_organization, year.
   - Example: [{{"name": "Certified Kubernetes Administrator",
     "issuing_organization": "CNCF", "year": "2021"}}]

7. **Projects:**
   - Extract all projects mentioned.
   - Return as a list of dictionaries.
   - Keys: name, description, technologies.
   - technologies should be a list of strings.
   - Example: [{{"name": "Resume Scanner", "description":
     "Parse resumes", "technologies": ["Python", "FastAPI"]}}]

**Important Instructions:**

- Carefully search through the entire resume for contact information.
- Look for email addresses in various formats and locations.
- Extract phone numbers even if they are in different formats.
- For work experience, extract all job positions and their details.
- Include all responsibilities and achievements for each position.
- If a field is not found, return null or empty list.
- Return ONLY valid JSON, no markdown or extra text.
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
