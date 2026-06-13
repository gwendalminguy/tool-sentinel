"""
sentinel/tools/list_directory.py
ListDirectory Tool Definition
"""
import os


class ListDirectory():
    """
    ListDirectory Tool Definition
    """
    name = "list_directory"
    description = "List the content of a directory."

    def execute(self, path: str) -> list[dict]:
        entries = []
        content = os.listdir(path)

        for item in content:
            full_path = os.path.join(path, item)

            entries.append({
                "name": item,
                "path": full_path,
                "type": "directory" if os.path.isdir(full_path) else "file"
            })

        return entries
