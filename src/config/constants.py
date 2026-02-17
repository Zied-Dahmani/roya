"""
Application constants.
"""

from enum import Enum


class SheetColumn(int, Enum):
    """Google Sheet column indices (0-indexed)."""
    NAME = 0
    PHONE = 1
    PRODUCT = 2
    LAST_VISIT = 3
    SMS_SENT = 4
    CHAT_HISTORY = 5


class MessageType(str, Enum):
    """Type of SMS message to generate."""
    FIRST = "first"
    FOLLOWUP = "followup"


SHEET_HEADERS = ["Name", "Phone", "Product", "Last Visit", "SMS Sent", "Chat History"]
MAX_SMS_LENGTH = 160
