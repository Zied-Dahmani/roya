"""
Prompt template for generating follow-up SMS messages.
"""

SYSTEM_PROMPT = """You are a direct but friendly sales assistant.
Reply naturally to what the customer said. Be specific and helpful.
No fluff. Keep it short like a real text message."""

USER_PROMPT = """Reply to {name}'s message about the {product}.

Their reply: "{latest_reply}"

Previous conversation:
{chat_history}

Rules:
- Directly address what they said
- Keep under 140 characters
- Be helpful and specific
- If they asked a question, answer it
- If they're interested, suggest next step (visit, call, etc.)
- If they're not interested, be polite and don't push

Output ONLY the SMS text."""


def build_followup_prompt(
    name: str,
    product: str,
    chat_history: str,
    latest_reply: str
) -> dict:
    """Build the prompt for generating a follow-up message."""
    return {
        "system": SYSTEM_PROMPT,
        "user": USER_PROMPT.format(
            name=name,
            product=product,
            chat_history=chat_history or "No previous messages",
            latest_reply=latest_reply or "No reply yet"
        )
    }
