"""
sentinel/tools/find_definition.py
FindDefinition Tool Definition
"""
from sentinel.utils.filesystem import iter_files

import ast
import os


class FindDefinition():
    """
    FindDefinition Tool Definition
    """
    name = "find_definition"
    description = "Find the definition of a class or function."

    def execute(self, path: str, query: str) -> list[dict]:
        results = []
        query_lower = query.lower()

        for file_path in iter_files(path):
            if not file_path.endswith(".py"):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    source = file.read()
                    lines = source.splitlines()

                    tree = ast.parse(source)

                    for node in ast.walk(tree):
                        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                            continue

                        if node.name.lower() != query_lower:
                            continue

                        node_type = "class" if isinstance(node, ast.ClassDef) else "function"

                        start = node.lineno
                        end = node.end_lineno
                        
                        definition = "\n".join(lines[start - 1:end])

                        results.append({
                            "path": file_path,
                            "name": node.name,
                            "type": node_type,
                            "start_line": start,
                            "end_line": end,
                            "docstring": ast.get_docstring(node),
                            "definition": definition
                        })
            except (UnicodeDecodeError, OSError, SyntaxError):
                continue

        return results
