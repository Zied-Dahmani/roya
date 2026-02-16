"""
Input validation utilities.
"""

import re


def is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid (basic check)."""
    digits = "".join(c for c in phone if c.isdigit())
    return 10 <= len(digits) <= 15


def is_valid_lead(lead) -> tuple[bool, str]:
    """
    Validate a lead has required fields.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not lead.name or not lead.name.strip():
        return False, "Lead missing name"

    if not lead.phone or not is_valid_phone(lead.phone):
        return False, f"Invalid phone for {lead.name}"

    if not lead.product or not lead.product.strip():
        return False, f"Lead {lead.name} missing product interest"

    return True, ""
