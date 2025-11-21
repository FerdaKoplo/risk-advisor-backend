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
            "prompt": prompt,
            "stream": False  
        }

        response = requests.post(self.base_url, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")

        try:
            data = response.json()
            if "response" in data:
                return str(data["response"]).strip()
            elif "responses" in data and isinstance(data["responses"], list):
                return " ".join(str(r).strip() for r in data["responses"])
            else:
                return str(response.text).strip()
        except ValueError:
            return str(response.text).strip()
