"""
LangGraph node functions for the SMS agent.
"""

from src.agent.state import AgentState
from src.config import MessageType
from src.services import GroqClient
from src.prompts import build_first_message_prompt, build_followup_prompt
from src.utils import format_chat_history, append_to_history


def classify_message_type(state: AgentState) -> AgentState:
    """Determine if this is a first message or follow-up."""
    lead = state["lead"]

    if lead.has_chat_history:
        state["message_type"] = MessageType.FOLLOWUP.value
    else:
        state["message_type"] = MessageType.FIRST.value

    return state


def generate_sms(state: AgentState, groq_client: GroqClient) -> AgentState:
    """Generate the SMS message using Groq."""
    lead = state["lead"]
    message_type = state["message_type"]

    try:
        if message_type == MessageType.FIRST.value:
            prompt = build_first_message_prompt(
                name=lead.first_name,
                product=lead.product,
                last_visit=lead.last_visit or "recently"
            )
        else:
            prompt = build_followup_prompt(
                name=lead.first_name,
                product=lead.product,
                chat_history=format_chat_history(lead.chat_history)
            )

        sms = groq_client.generate(prompt["system"], prompt["user"])
        state["generated_sms"] = sms
        state["error"] = None

    except Exception as e:
        state["error"] = str(e)
        state["generated_sms"] = None

    return state


def update_history(state: AgentState) -> AgentState:
    """Update chat history with the new message."""
    if state["generated_sms"]:
        lead = state["lead"]
        new_history = append_to_history(
            existing_history=lead.chat_history,
            role="assistant",
            message=state["generated_sms"]
        )
        state["updated_history"] = new_history

    return state
