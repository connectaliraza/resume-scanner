"""
This module provides utilities for extracting structured data from resume text
using Google Gemini.
"""
import os

import google.generativeai as genai


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

Return the extracted information in JSON format.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during Gemini extraction: {e}")
        return {}
