"""
This module provides utilities for transforming data to match expected formats.
"""


def transform_skills_to_list(skills_data) -> list[str]:
    """
    Transforms skills data from a dictionary or other formats to a flat list of strings.
    """
    if isinstance(skills_data, list):
        return skills_data  # Already in the correct format

    if not isinstance(skills_data, dict):
        return []  # Return empty list if not a dictionary or list

    skill_list = []
    for key, value in skills_data.items():
        if isinstance(value, list):
            skill_list.extend(value)
        elif isinstance(value, str):
            skill_list.append(value)
        else:
            # If the value is neither a list nor a string, just add the key
            skill_list.append(key)

    return skill_list
