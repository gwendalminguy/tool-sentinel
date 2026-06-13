"""
sentinel/llm/client.py
Ollama LLM Client Definition
"""
from ollama import Client
from sentinel.config import OLLAMA_MODEL, OLLAMA_HOST


class OllamaClient():
    def __init__(self, model: str = OLLAMA_MODEL, host: str = OLLAMA_HOST, system_prompt: str = ""):
        self.client = Client(host=host)
        self.model = model
        self.system_prompt = system_prompt
    
    def generate(self, prompt: str | None = None, messages: list | None = None) -> str:
        if messages is None:
            messages = []

            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

        response = self.client.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]
