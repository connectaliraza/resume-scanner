"""
This module provides utilities for extracting structured data from resume text
using an LLM.
"""
import os

from openai import OpenAI


def extract_with_llm(resume_text: str) -> dict:
    """Extracts structured data from resume text using an LLM."""
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

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
        system_msg = (
            "You are a helpful assistant that extracts information from resumes."
        )
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM extraction: {e}")
        return {}
