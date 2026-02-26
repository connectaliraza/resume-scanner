"""
This module provides a simple in-memory database abstraction.
"""
from typing import Any, Dict, List


class Database:
    """A simple in-memory database."""

    def __init__(self):
        self._data: Dict[str, List[Dict[str, Any]]] = {
            "resumes": [],
            "parsed_resumes": [],
        }

    def get_all(self, table: str) -> List[Dict[str, Any]]:
        """Returns all records from a table."""
        return self._data.get(table, [])

    def get_by_id(self, table: str, record_id: int) -> Dict[str, Any] | None:
        """Returns a record by its ID."""
        for record in self.get_all(table):
            if record.get("id") == record_id:
                return record
        return None

    def add(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a new record to a table."""
        record_id = len(self.get_all(table)) + 1
        record["id"] = record_id
        self._data[table].append(record)
        return record
