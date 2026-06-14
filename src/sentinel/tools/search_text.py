"""
sentinel/tools/search_text.py
SearchText Tool Definition
"""
from sentinel.utils.filesystem import iter_files

import os


class SearchText():
    """
    SearchText Tool Definition
    """
    name = "search_text"
    description = "Search for a text pattern in files."

    def execute(self, path: str, query: str) -> list[dict]:
        results = []
        query_lower = query.lower()

        for file_path in iter_files(path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    for i, line in enumerate(file, start=1):
                        if query_lower in line.lower():
                            results.append({
                                "path": file_path,
                                "line": i,
                                "content": line.strip()
                            })
            except (UnicodeDecodeError, OSError):
                continue

        return results
