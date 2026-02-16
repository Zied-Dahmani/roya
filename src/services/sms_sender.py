"""
Twilio SMS sender for sending messages.
"""

from twilio.rest import Client
from src.config import Settings


class SMSSender:
    """Sends SMS via Twilio."""

    def __init__(self, settings: Settings):
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self.from_number = settings.twilio_phone_number

    def send(self, to: str, message: str) -> str:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number (E.164 format, e.g., +1234567890)
            message: SMS text to send

        Returns:
            Message SID if successful
        """
        # Clean phone number to E.164 format
        to_clean = self._format_phone(to)

        result = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_clean
        )
        return result.sid

    @staticmethod
    def _format_phone(phone: str) -> str:
        """Format phone to E.164 (+countrycode...)."""
        digits = "".join(c for c in phone if c.isdigit())
        if not digits.startswith("+"):
            digits = "+" + digits
        return digits
