"""
Application settings loaded from environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings container."""

    # Google Sheets
    google_sheet_id: str
    google_credentials_path: str
    worksheet_name: str

    # Groq AI
    groq_api_key: Optional[str]
    model_name: str
    max_tokens: int
    temperature: float

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        google_sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not google_sheet_id:
            raise ValueError("GOOGLE_SHEET_ID is required")

        return cls(
            google_sheet_id=google_sheet_id,
            google_credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"),
            worksheet_name=os.getenv("WORKSHEET_NAME", "Sheet1"),
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=os.getenv("AI_MODEL", "llama-3.1-8b-instant"),
            max_tokens=int(os.getenv("MAX_TOKENS", "150")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
        )


def get_settings() -> Settings:
    """Factory function to get settings instance."""
    return Settings.from_env()
