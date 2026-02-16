"""
Message and data formatting utilities.
"""

from datetime import datetime
from src.config import MAX_SMS_LENGTH


def format_chat_history(history: str | None) -> str:
    """Format chat history for prompt inclusion."""
    if not history or not history.strip():
        return "No previous conversation."
    return history.strip()


def append_to_history(existing_history: str | None, role: str, message: str) -> str:
    """
    Append a new message to chat history.

    Args:
        existing_history: Current chat history string
        role: "assistant" or "customer"
        message: The message to append

    Returns:
        Updated history string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"[{timestamp}] {role.upper()}: {message}"

    if existing_history and existing_history.strip():
        return f"{existing_history.strip()}\n{new_entry}"
    return new_entry


def truncate_sms(message: str, max_length: int = MAX_SMS_LENGTH) -> str:
    """Truncate SMS to max length if needed."""
    if len(message) <= max_length:
        return message
    return message[:max_length - 3] + "..."


def format_phone(phone: str) -> str:
    """Clean and format phone number."""
    digits = "".join(c for c in phone if c.isdigit())
    return digits
