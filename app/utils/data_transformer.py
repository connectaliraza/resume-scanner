"""
This module provides utilities for transforming data to match expected formats.
"""


def transform_to_list_of_dicts(data) -> list[dict]:
    """
    Transforms data from a list of strings or other formats to a list of dictionaries.
    """
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return data  # Already in the correct format

        # Convert list of strings to list of dictionaries
        return [{"description": str(item)} for item in data]

    if isinstance(data, dict):
        # Convert dictionary to a list of one dictionary
        return [data]

    return []  # Return empty list for other types


def transform_skills_to_list(skills_data) -> list[str]:
    """
    Transforms skills data from a dictionary or other formats to a flat list of strings.
    """
    if isinstance(skills_data, list):
        return [str(item) for item in skills_data]

    if not isinstance(skills_data, dict):
        return []

    skill_list = []
    for key, value in skills_data.items():
        if isinstance(value, list):
            skill_list.extend([str(item) for item in value])
        elif isinstance(value, str):
            skill_list.append(value)
        else:
            skill_list.append(key)

    return skill_list


def transform_work_experience(experience_data) -> list[dict]:
    """
    Transforms work experience data to a list of dictionaries.
    Handles cases where Gemini returns a single dictionary or a list of strings.
    """
    if isinstance(experience_data, list):
        if all(isinstance(item, dict) for item in experience_data):
            return experience_data  # Already in the correct format

        # Convert list of strings to list of dictionaries
        return [{"description": str(item)} for item in experience_data]

    if isinstance(experience_data, dict):
        # Convert single dictionary to a list of one dictionary
        return [experience_data]

    return []
