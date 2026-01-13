# llm_client.py

import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Always load .env from the SAME folder as this file (works in Streamlit too)
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)


class BaseLLMClient:
    def generate(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError


class OpenRouterLLMClient(BaseLLMClient):
    def __init__(self, temperature: float = 0.2):
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        model = os.getenv("OPENROUTER_MODEL", "").strip()

        # Hard fails (so you don't get confusing 401s later)
        if not api_key:
            raise RuntimeError(f"OPENROUTER_API_KEY is missing. Checked: {ENV_PATH}")
        if not api_key.startswith("sk-"):
            raise RuntimeError("OPENROUTER_API_KEY looks wrong (should start with sk-). Remove quotes/spaces.")
        if not model:
            raise RuntimeError(f"OPENROUTER_MODEL is missing. Checked: {ENV_PATH}")

        self.temperature = float(temperature)
        self.model = model

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        self.extra_headers = {
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost").strip(),
            "X-Title": os.getenv("OPENROUTER_APP_NAME", "SOC Incident Trainer").strip(),
        }

    def generate(self, messages: List[Dict[str, str]]) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            extra_headers=self.extra_headers,
        )
        return resp.choices[0].message.content
