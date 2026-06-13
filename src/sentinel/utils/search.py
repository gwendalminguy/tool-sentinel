"""
sentinel/utils/search.py
Search Utility Functions
"""
import os


def group_results(results: list[dict]) -> list[dict]:
    """
    Group search results by file.
    """
    groups = {}

    for item in results:
        path = item["path"]

        if path not in groups:
            groups[path] = []

        groups[path].append({
            "line": item["line"],
            "content": item["content"]
        })

    elements = [{"path": path, "occurences": occurence} for path, occurence in groups.items()]

    return elements
        
