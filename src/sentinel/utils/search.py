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

    elements = [{"path": path, "occurrences": occurrence} for path, occurrence in groups.items()]

    return elements


def score_result(result: dict, query: str) -> int:
    """
    Score pertinence of a search result.
    """
    score = 0

    content = result["content"].lower()
    stripped = content.strip()
    symbol = query.lower()

    if stripped.startswith(f"class {symbol}"):
        score += 150

    if stripped.startswith(f"def {symbol}"):
        score += 100

    if (f"{symbol}(" in content
        and not stripped.startswith("class ")
        and not stripped.startswith("def ")
    ):
        score += 50

    if stripped.startswith("import ") or stripped.startswith("from "):
        score += 25

    if result["path"].endswith(".py"):
        score += 10

    return score


def rank_results(results: list[dict], query: str, top: int = 5) -> list[dict]:
    """
    Rank search results by score.
    """
    for result in results:
        result["score"] = score_result(result, query)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results[:top]
