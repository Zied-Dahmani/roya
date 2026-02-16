"""
Prompt template for generating follow-up SMS messages.
"""

SYSTEM_PROMPT = """You are a friendly sales assistant continuing a conversation.
Your goal is to maintain rapport and be genuinely helpful.
Respond naturally based on the conversation history.
Never ignore what the customer said - always acknowledge their input."""

USER_PROMPT = """Generate a follow-up SMS based on the conversation history.

Lead Information:
- Name: {name}
- Product of Interest: {product}

Conversation History:
{chat_history}

Customer's Latest Reply:
{latest_reply}

Requirements:
- Keep under 160 characters
- Continue naturally from the conversation
- Address any questions or concerns they raised
- Be helpful and friendly, not pushy
- Move the conversation forward appropriately

Output ONLY the SMS text, nothing else."""


def build_followup_prompt(
    name: str,
    product: str,
    chat_history: str,
    latest_reply: str
) -> dict:
    """
    Build the prompt for generating a follow-up message.

    Args:
        name: Customer's name
        product: Product they showed interest in
        chat_history: Previous conversation history
        latest_reply: Customer's most recent reply

    Returns:
        Dict with 'system' and 'user' prompt strings
    """
    return {
        "system": SYSTEM_PROMPT,
        "user": USER_PROMPT.format(
            name=name,
            product=product,
            chat_history=chat_history or "No previous messages",
            latest_reply=latest_reply or "No reply yet"
        )
    }
