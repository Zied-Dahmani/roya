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
    REPLY = 5
    CHAT_HISTORY = 6


class MessageType(str, Enum):
    """Type of SMS message to generate."""
    FIRST = "first"
    FOLLOWUP = "followup"


SHEET_HEADERS = ["Name", "Phone", "Product", "Last Visit", "SMS Sent", "Reply", "Chat History"]
MAX_SMS_LENGTH = 160
