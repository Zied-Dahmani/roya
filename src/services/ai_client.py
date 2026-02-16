"""
Groq AI client for generating SMS messages.
"""

import httpx
from src.config import Settings


class GroqClient:
    """Client for Groq API (OpenAI-compatible)."""

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, settings: Settings):
        self.api_key = settings.groq_api_key
        self.model = settings.model_name
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature

        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a response using Groq.

        Args:
            system_prompt: System instructions for the AI
            user_prompt: User message/request

        Returns:
            Generated text response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(self.BASE_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
