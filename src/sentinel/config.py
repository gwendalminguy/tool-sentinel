"""
sentinel/config.py
Variables and environment configuration.
"""
from dotenv import load_dotenv

import os


load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
