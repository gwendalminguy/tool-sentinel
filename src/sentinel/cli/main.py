"""
sentinel/cli/main.py
Sentinel CLI Entry Point
"""
from sentinel.llm.client import OllamaClient

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
        response = client.generate(prompt)

        print(response)


@app.command()
def chat():
    """
    Start an interactive chat session with the LLM.
    """
    client = OllamaClient()

    print("Sentinel Interactive Chat Mode ('/exit' to quit)")

    while True:
        prompt = input("> ")

        if prompt.strip().lower() == "/exit":
            break
        elif prompt.strip().lower() == "/clear":
            os.system("clear")
            continue

        if not prompt.strip():
            continue

        response = client.generate(prompt)

        print(f"> {response}")


if __name__ == "__main__":
    app()
