"""
Prompt template for generating first contact SMS messages.
"""

SYSTEM_PROMPT = """You are a friendly sales assistant for a retail business.
Your goal is to craft warm, personalized SMS messages that feel genuine and helpful.
Never be pushy or overly salesy. Sound like a helpful friend, not a marketer."""

USER_PROMPT = """Generate a first SMS message to a potential customer.

Lead Information:
- Name: {name}
- Product of Interest: {product}
- Last Visit: {last_visit}

Requirements:
- Keep under 160 characters
- Use their first name naturally
- Reference their product interest subtly
- Include a soft, non-pushy call-to-action
- Sound warm and conversational

Output ONLY the SMS text, nothing else."""


def build_first_message_prompt(name: str, product: str, last_visit: str) -> dict:
    """
    Build the prompt for generating a first contact message.

    Args:
        name: Customer's name
        product: Product they showed interest in
        last_visit: Date of their last visit

    Returns:
        Dict with 'system' and 'user' prompt strings
    """
    return {
        "system": SYSTEM_PROMPT,
        "user": USER_PROMPT.format(
            name=name,
            product=product,
            last_visit=last_visit or "Unknown"
        )
    }
