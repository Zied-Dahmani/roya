"""
Lead data model representing a row from Google Sheets.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Lead:
    """Represents a lead from the Google Sheet."""

    row_number: int
    name: str
    phone: str
    product: str
    last_visit: Optional[str] = None
    sms_sent: Optional[str] = None
    reply: Optional[str] = None
    chat_history: Optional[str] = None

    @property
    def first_name(self) -> str:
        """Extract first name from full name."""
        return self.name.split()[0] if self.name else ""

    @property
    def has_been_contacted(self) -> bool:
        """Check if lead has received any SMS."""
        return bool(self.sms_sent and self.sms_sent.strip())

    @property
    def has_replied(self) -> bool:
        """Check if lead has replied."""
        return bool(self.reply and self.reply.strip())

    @property
    def needs_followup(self) -> bool:
        """Check if lead needs a follow-up message."""
        return self.has_been_contacted and self.has_replied

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "row_number": self.row_number,
            "name": self.name,
            "phone": self.phone,
            "product": self.product,
            "last_visit": self.last_visit,
            "sms_sent": self.sms_sent,
            "reply": self.reply,
            "chat_history": self.chat_history,
        }

    @classmethod
    def from_row(cls, row_number: int, row_data: list) -> "Lead":
        """
        Create Lead from a Google Sheets row.

        Args:
            row_number: The row number in the sheet (1-indexed)
            row_data: List of cell values from the row

        Returns:
            Lead instance
        """
        def safe_get(index: int) -> Optional[str]:
            try:
                value = row_data[index]
                return str(value).strip() if value else None
            except IndexError:
                return None

        return cls(
            row_number=row_number,
            name=safe_get(0) or "",
            phone=safe_get(1) or "",
            product=safe_get(2) or "",
            last_visit=safe_get(3),
            sms_sent=safe_get(4),
            reply=safe_get(5),
            chat_history=safe_get(6),
        )
