"""
sentinel/utils/context.py
Context Utility Functions
"""
import os


def build_code_context(groups: list[dict]) -> str:
    """
    Build context around each line of code of a list.
    """
    result = ""

    for group in groups:
        path = group["path"]

        result += f"\nFILE: {path}\n"

        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            for occurrence in group["occurrences"]:
                line = occurrence["line"]
                start = max(1, line - 5)
                end = min(len(lines), line + 5)

                result += f"\nMATCH LINE: {line}\n"

                for i in range(start - 1, end):
                    result += f"{i+1:4} | {lines[i]}"

    return result
