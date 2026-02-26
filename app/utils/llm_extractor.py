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
    transform_work_experience,
)


def _normalize_keys(data: dict) -> dict:
    """Converts dictionary keys from title/space case to snake_case."""
    normalized_data = {}
    for key, value in data.items():
        if key == "Contact Information":
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    normalized_sub_key = sub_key.lower().replace(" ", "_")
                    normalized_data[normalized_sub_key] = sub_value
        else:
            normalized_key = key.lower().replace(" ", "_")
            normalized_data[normalized_key] = value
    return normalized_data


def extract_with_llm(resume_text: str) -> dict:
    """Extracts structured data from resume text using Google Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return {}

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

1.  **Full Name:**
    -   Extract the full name of the candidate.
    -   Example: "John Doe"

2.  **Email:**
    -   Extract the primary email address.
    -   Look for email patterns like name@domain.com.

3.  **Phone:**
    -   Extract the primary phone number.
    -   Look for phone patterns with digits and common separators.

4.  **Skills:**
    -   Extract all technical and soft skills mentioned.
    -   Return as a flat list of strings.
    -   Example: ["Python", "FastAPI", "Teamwork"]

5.  **Education:**
    -   Extract all educational qualifications.
    -   Return as a list of dictionaries.
    -   Keys: degree, institution, year.
    -   Example: [{{"degree": "Bachelor of Science", "institution":
     "University", "year": "2020"}}]

6.  **Work Experience:**
    -   Extract all work experience entries from sections like "Work
      Experience", "Employment History", "Professional Experience",
      "Career History", or "Work History".
    -   Return as a list of dictionaries.
    -   Keys: job_title, company, duration, responsibilities.
    -   responsibilities should be a list of strings.
    -   Example: [{{"job_title": "Software Engineer", "company":
     "Tech Corp", "duration": "2020-2022", "responsibilities":
     ["Developed features", "Fixed bugs"]}}]

7.  **Certifications:**
    -   Extract all certifications and licenses.
    -   Return as a list of dictionaries.
    -   Keys: name, issuing_organization, year.
    -   Example: [{{"name": "Certified Kubernetes Administrator",
     "issuing_organization": "CNCF", "year": "2021"}}]

8.  **Projects:**
    -   Extract all projects mentioned.
    -   Return as a list of dictionaries.
    -   Keys: name, description, technologies.
    -   technologies should be a list of strings.
    -   Example: [{{"name": "Resume Scanner", "description":
     "Parse resumes", "technologies": ["Python", "FastAPI"]}}]

**Important Instructions:**

-   Carefully search through the entire resume for contact information.
-   Look for email addresses in various formats and locations.
-   Extract phone numbers even if they are in different formats.
-   For work experience, extract all job positions and their details.
-   Include all responsibilities and achievements for each position.
-   If a field is not found, return null or empty list.
-   Return ONLY valid JSON, no markdown or extra text.
"""

    try:
        response = model.generate_content(prompt)

        if not response.text or not response.text.strip():
            print("Error: Gemini returned an empty response.")
            return {}

        # Clean the response to remove markdown formatting
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]

        parsed_json = json.loads(cleaned_text)
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
            normalized_data["work_experience"] = transform_work_experience(
                normalized_data["work_experience"]
            )
        if "certifications" in normalized_data:
            normalized_data["certifications"] = transform_to_list_of_dicts(
                normalized_data["certifications"]
            )

        return normalized_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Gemini: {e}")
        print(f"Raw Gemini response: {response.text}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
