"""
sentinel/cli/main.py
Sentinel CLI Entry Point
"""
from sentinel.llm.client import OllamaClient
from sentinel.tools.list_directory import ListDirectory
from sentinel.tools.read_file import ReadFile
from sentinel.tools.search_text import SearchText
from rich import print
from typing import Annotated

import os
import typer


app = typer.Typer()

@app.command()
def ask(prompt: str = typer.Argument(..., help="Question to ask to the LLM.")):
    """
    Ask the LLM a question and print the response.
    """
    client = OllamaClient()

    if prompt.strip():
        response = client.generate(prompt=prompt)

        print(response)


@app.command()
def chat():
    """
    Start an interactive chat session with the LLM.
    """
    client = OllamaClient()

    history = []

    print("Sentinel Interactive Chat Mode ('/exit' to quit)")

    while True:
        prompt = input("> ")

        if prompt.strip().lower() == "/exit":
            break
        elif prompt.strip().lower() == "/clear":
            os.system("clear")
            history = []
            continue

        if not prompt.strip():
            continue

        history.append({"role": "user", "content": prompt})

        response = client.generate(messages=history)

        history.append({"role": "assistant", "content": response})

        print(f"> {response}")


@app.command()
def read(
    path: str, 
    start: Annotated[int, typer.Argument()] = None,
    end: Annotated[int, typer.Argument()] = None,
):
    """
    Read the content of a file from disk.
    """
    tool = ReadFile()
    path = os.path.abspath(path)

    content = tool.execute(path, start, end)
    print(content)


@app.command()
def ls(path: str):
    """
    List the content of a directory.
    """
    tool = ListDirectory()
    path = os.path.abspath(path)

    elements = tool.execute(path)
    print(elements)


@app.command()
def search(path: str, query: str):
    """
    Search for a text pattern in files.
    """
    tool = SearchText()
    path = os.path.abspath(path)

    elements = tool.execute(path, query)
    print(elements)


if __name__ == "__main__":
    app()
