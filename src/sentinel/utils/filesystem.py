"""
sentinel/utils/filesystem.py
FileSystem Utility Functions
"""
from collections.abc import Iterator

import os


def iter_files(path: str) -> Iterator[str]:
    """
    Yield all file paths from a directory tree.

    If `path` is a directory, recursively yields all file paths inside it.
    If `path` is a file, yields the file itself.
    """
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                yield os.path.join(root, file)

    else:
        yield path
