"""
sentinel/utils/filesystem.py
FileSystem Utility Functions
"""
from collections.abc import Iterator

import os


IGNORE_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
}

VALID_EXTENSIONS = {
    ".py",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
}


def iter_files(path: str) -> Iterator[str]:
    """
    Yield all file paths from a directory tree.

    If `path` is a directory, recursively yields all file paths inside it.
    If `path` is a file, yields the file itself.
    """
    if os.path.isdir(path):
        for root, directories, files in os.walk(path):
            directories[:] = [d for d in directories if d not in IGNORE_DIRECTORIES]
            for file in files:
                if os.path.splitext(file)[1] not in VALID_EXTENSIONS:
                    continue

                yield os.path.join(root, file)

    else:
        yield path
