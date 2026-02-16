"""
Roya SMS Agent - Entry Point

Run manually to process leads and generate SMS messages.
"""

import sys
from dotenv import load_dotenv

from src.config import get_settings
from src.services import SheetHandler, GroqClient
from src.agent import run_agent
from src.utils import is_valid_lead, truncate_sms


def print_banner():
    """Print application banner."""
    print("\n" + "=" * 50)
    print("  ROYA - AI SMS Agent")
    print("=" * 50 + "\n")


def print_sms_output(lead, result):
    """Display generated SMS for manual sending."""
    print("-" * 40)
    print(f"TO: {lead.name} ({lead.phone})")
    print(f"PRODUCT: {lead.product}")
    print(f"TYPE: {result['message_type'].upper()}")
    print("-" * 40)
    print(f"\nSMS MESSAGE:\n{result['generated_sms']}")
    print(f"\n[{len(result['generated_sms'])} characters]")
    print("-" * 40)


def process_lead(lead, groq_client, sheet_handler, auto_update: bool = False):
    """Process a single lead through the agent."""
    # Validate lead
    is_valid, error = is_valid_lead(lead)
    if not is_valid:
        print(f"Skipping: {error}")
        return False

    # Run agent
    result = run_agent(lead, groq_client)

    if result["error"]:
        print(f"Error processing {lead.name}: {result['error']}")
        return False

    # Display SMS for manual sending
    print_sms_output(lead, result)

    # Update sheet if requested
    if auto_update and result["generated_sms"]:
        sheet_handler.batch_update(
            row_number=lead.row_number,
            sms_sent=result["generated_sms"],
            chat_history=result["updated_history"]
        )
        print("[Sheet updated]")

    return True


def main():
    """Main entry point."""
    load_dotenv()
    print_banner()

    try:
        settings = get_settings()
        sheet_handler = SheetHandler(settings)
        groq_client = GroqClient(settings)

        print("Connecting to Google Sheet...")
        sheet_handler.connect()

        # Get leads needing attention
        new_leads = sheet_handler.get_leads_needing_contact()
        followup_leads = sheet_handler.get_leads_needing_followup()

        print(f"Found {len(new_leads)} new leads")
        print(f"Found {len(followup_leads)} leads needing follow-up\n")

        # Process new leads first
        if new_leads:
            print("\n=== NEW LEADS ===\n")
            for lead in new_leads:
                process_lead(lead, groq_client, sheet_handler)
                print()

        # Then follow-ups
        if followup_leads:
            print("\n=== FOLLOW-UPS ===\n")
            for lead in followup_leads:
                process_lead(lead, groq_client, sheet_handler)
                print()

        if not new_leads and not followup_leads:
            print("No leads to process.")

        print("\nDone!")

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
