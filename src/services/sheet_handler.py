"""
Google Sheets integration for reading and writing lead data.
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Optional

from src.config import Settings, SheetColumn
from src.models import Lead


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class SheetHandler:
    """Handles all Google Sheets operations."""

    def __init__(self, settings: Settings):
        """
        Initialize the sheet handler.

        Args:
            settings: Application settings containing credentials path and sheet ID
        """
        self.settings = settings
        self._client: Optional[gspread.Client] = None
        self._sheet: Optional[gspread.Spreadsheet] = None
        self._worksheet: Optional[gspread.Worksheet] = None

    def connect(self) -> None:
        """Establish connection to Google Sheets."""
        credentials = Credentials.from_service_account_file(
            self.settings.google_credentials_path,
            scopes=SCOPES
        )
        self._client = gspread.authorize(credentials)
        self._sheet = self._client.open_by_key(self.settings.google_sheet_id)
        self._worksheet = self._sheet.worksheet(self.settings.worksheet_name)

    @property
    def worksheet(self) -> gspread.Worksheet:
        """Get the active worksheet, connecting if needed."""
        if self._worksheet is None:
            self.connect()
        return self._worksheet

    def get_all_leads(self) -> List[Lead]:
        """
        Fetch all leads from the sheet.

        Returns:
            List of Lead objects (excludes header row)
        """
        rows = self.worksheet.get_all_values()
        leads = []

        # Skip header row (index 0), start from row 2 in sheet terms
        for i, row in enumerate(rows[1:], start=2):
            if row[0]:  # Only include rows with a name
                leads.append(Lead.from_row(i, row))

        return leads

    def get_lead_by_row(self, row_number: int) -> Optional[Lead]:
        """
        Fetch a specific lead by row number.

        Args:
            row_number: The row number (1-indexed, 1 is header)

        Returns:
            Lead object or None if row is empty
        """
        row_data = self.worksheet.row_values(row_number)
        if row_data and row_data[0]:
            return Lead.from_row(row_number, row_data)
        return None

    def get_leads_needing_contact(self) -> List[Lead]:
        """
        Get leads that haven't been contacted yet.

        Returns:
            List of leads with no SMS sent
        """
        return [lead for lead in self.get_all_leads() if not lead.has_been_contacted]

    def get_leads_needing_followup(self) -> List[Lead]:
        """
        Get leads that need a follow-up message.

        Returns:
            List of leads who have replied and need follow-up
        """
        return [lead for lead in self.get_all_leads() if lead.needs_followup]

    def update_sms_sent(self, row_number: int, message: str) -> None:
        """
        Update the SMS Sent column for a lead.

        Args:
            row_number: The row to update
            message: The SMS message that was sent
        """
        col = SheetColumn.SMS_SENT.value + 1  # gspread uses 1-indexed columns
        self.worksheet.update_cell(row_number, col, message)

    def update_chat_history(self, row_number: int, history: str) -> None:
        """
        Update the Chat History column for a lead.

        Args:
            row_number: The row to update
            history: The updated chat history string
        """
        col = SheetColumn.CHAT_HISTORY.value + 1
        self.worksheet.update_cell(row_number, col, history)

    def batch_update(self, row_number: int, sms_sent: str, chat_history: str) -> None:
        """
        Update both SMS Sent and Chat History in one API call.

        Args:
            row_number: The row to update
            sms_sent: The SMS message sent
            chat_history: The updated chat history
        """
        sms_col = SheetColumn.SMS_SENT.value + 1
        history_col = SheetColumn.CHAT_HISTORY.value + 1

        self.worksheet.update(f"{self._col_letter(sms_col)}{row_number}", [[sms_sent]])
        self.worksheet.update(f"{self._col_letter(history_col)}{row_number}", [[chat_history]])

    @staticmethod
    def _col_letter(col_num: int) -> str:
        """Convert column number to letter (1=A, 2=B, etc.)."""
        result = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num - 1, 26)
            result = chr(65 + remainder) + result
        return result
