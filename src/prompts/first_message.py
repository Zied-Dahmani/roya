"""
Prompt template for generating first contact SMS messages.
"""

SYSTEM_PROMPT = """You are a direct but friendly sales assistant.
Write short, specific SMS messages that mention the exact product.
No fluff. Get to the point. Be casual like texting a friend."""

USER_PROMPT = """Write a short SMS to {name} about the {product} they wanted.

Examples of good messages:
- "Hey {name}! Still interested in that {product}? We just got new stock in 🔥"
- "Hi {name}, the {product} you liked is still available. Want me to hold one for you?"
- "Hey {name}! New {product} models just arrived. Thought of you - want to check them out?"

Rules:
- MUST mention the specific product ({product})
- Under 140 characters
- Casual, friendly tone
- One clear question or call-to-action
- No generic greetings like "hope you're doing well"

Output ONLY the SMS text."""


def build_first_message_prompt(name: str, product: str, last_visit: str) -> dict:
    """Build the prompt for generating a first contact message."""
    return {
        "system": SYSTEM_PROMPT,
        "user": USER_PROMPT.format(name=name, product=product)
    }
