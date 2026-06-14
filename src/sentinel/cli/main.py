"""
sentinel/cli/main.py
Sentinel CLI Entry Point
"""
from sentinel.llm.client import OllamaClient
from sentinel.tools.find_definition import FindDefinition
from sentinel.tools.list_directory import ListDirectory
from sentinel.tools.read_file import ReadFile
from sentinel.tools.search_text import SearchText
from sentinel.utils.context import build_code_context
from sentinel.utils.search import group_results, rank_results
from rich import print
from typing import Annotated

import os
import typer


app = typer.Typer()

@app.command()
def ask(
    prompt: Annotated[str, typer.Argument(help="Question to ask to the LLM.")]
):
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

    print("\nSentinel Interactive Chat Mode ('/exit' to quit)")

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
    path: Annotated[str, typer.Argument(help="Path of the file to read.")], 
    start: Annotated[int | None, typer.Option("--start", "-s", help="Start line number.")] = None,
    end: Annotated[int | None, typer.Option("--end", "-e", help="End line number.")] = None
):
    """
    Read the content of a file from disk.
    """
    tool = ReadFile()
    path = os.path.abspath(path)

    content = tool.execute(path, start, end)

    if not content:
        print(f"No content found.")
        return

    print(content)


@app.command()
def ls(
    path: Annotated[str, typer.Argument(help="Path of the directory to list.")]
):
    """
    List the content of a directory.
    """
    tool = ListDirectory()
    path = os.path.abspath(path)

    elements = tool.execute(path)

    print(elements)


@app.command()
def search(
    path: Annotated[str, typer.Argument(help="Path of the directory or file to search for the pattern.")],
    query: Annotated[str, typer.Argument(help="Pattern to search for.")]
):
    """
    Search for a text pattern in files.
    """
    tool = SearchText()
    path = os.path.abspath(path)

    elements = tool.execute(path, query)

    print(elements)


@app.command()
def explain(
    path: Annotated[str, typer.Argument(help="Path of the directory to search for the symbol.")],
    symbol: Annotated[str, typer.Argument(help="Symbol to explain.")],
    top: Annotated[int, typer.Option("--top", "-t", help="Number of search results to analyze.")] = 5
):
    """
    Explain a symbol.
    """
    client = OllamaClient()

    tool = SearchText()
    path = os.path.abspath(path)

    elements = tool.execute(path, symbol)

    if not elements:
        print(f"No results found for symbol '{symbol}'.")
        return

    # Score and rank search results
    ranked = rank_results(elements, symbol, top)

    # Group results by file
    groups = group_results(ranked)

    # Build context by adding previous and next lines
    context = build_code_context(groups)

    prompt = f"""
    Explain the symbol '{symbol}' using the following code context.
    {context}
    """

    response = client.generate(prompt=prompt)

    print(response)


@app.command()
def find(
    path: Annotated[str, typer.Argument(help="Path of the directory to search for the symbol.")],
    symbol: Annotated[str, typer.Argument(help="Symbol to find.")]
):
    """
    Find a symbol definition.
    """
    client = OllamaClient()

    tool = FindDefinition()
    path = os.path.abspath(path)

    elements = tool.execute(path, symbol)

    if not elements:
        print(f"No results found for symbol '{symbol}'.")
        return

    print(elements)


if __name__ == "__main__":
    app()
