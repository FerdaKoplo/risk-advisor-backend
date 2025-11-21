import requests
import os
from dotenv import load_dotenv

load_dotenv() 

class OllamaService:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt
        }

        response = requests.post(self.base_url, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")

        return response.json().get("response", "").strip()
