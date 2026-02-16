"""
LangGraph agent state definition.
"""

from typing import TypedDict, Optional
from src.models import Lead


class AgentState(TypedDict):
    """State passed through the LangGraph flow."""

    lead: Lead
    message_type: str  # "first" or "followup"
    generated_sms: Optional[str]
    updated_history: Optional[str]
    error: Optional[str]
