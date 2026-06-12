"""
sentinel/cli/main.py
Sentinel CLI Entry Point
"""
from sentinel.llm.client import OllamaClient


def main():
    client = OllamaClient()
    response = client.generate("Hello.")
    print(response)


if __name__ == "__main__":
    main()
