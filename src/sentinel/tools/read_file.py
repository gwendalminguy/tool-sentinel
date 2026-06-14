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

    def execute(self, path: str, start: int = None, end: int = None) -> str:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            # Define start line
            if start is not None:
                start = max(1, start)
            else:
                start = 1

            # Define end line
            if end is not None:
                end = min(len(lines), end)
            else:
                end = len(lines)

            lines = lines[start-1:end]

            return "".join(lines)
