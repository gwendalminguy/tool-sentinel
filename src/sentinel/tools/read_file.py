"""
sentinel/tools/read_file.py
ReadFile Tool Definition
"""


class ReadFile():
    """
    ReadFile Tool Definition
    """
    name = "read_file"
    description = "Read the content of a file from disk."

    def execute(self, path: str) -> str:
        with open(path) as file:
            return file.read()
