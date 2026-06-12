"""
sentinel/cli/main.py
Sentinel CLI Entry Point
"""
from sentinel.llm.client import OllamaClient

import typer


app = typer.Typer()

@app.command()
def ask(prompt: str = typer.Argument(..., help="Question to ask to the LLM.")):
    """
    Ask the LLM a question and print the response.
    """
    client = OllamaClient()
    response = client.generate(prompt)

    print(response)


@app.command()
def chat():
    """
    Start an interactive chat session with the LLM.
    """
    client = OllamaClient()

    while True:
        prompt = input("> ")
        response = client.generate(prompt)

        print(f"> {response}")


if __name__ == "__main__":
    app()
