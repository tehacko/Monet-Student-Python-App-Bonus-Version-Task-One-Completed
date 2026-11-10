# -----------------------------
# REPOSITORY LAYER (database / storage details only)
# -----------------------------
# Swap this file to change storage (Google Sheets -> SQLite, CSV, etc.)
# without changing gui.py or logic.py.

# -----------------------------
# 1. IMPORTS
# -----------------------------
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError, SpreadsheetNotFound

# -----------------------------
# 2. SETUP (STORAGE SETTINGS)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

# Put your service account JSON next to this file (keep it out of git).
SERVICE_ACCOUNT_FILE = BASE_DIR / "shaped-terrain-494211-e7-8a83970f3746.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

# Update these for your own Google Drive folder / sheet.
FOLDER_ID = "1RxX80Imkk1n_pyu1GneC4VfYuS1A8nxo"
SHEET_NAME = "hajek_my_fat_data"

# -----------------------------
# 3. FUNCTIONS
# -----------------------------
def create_gspread_client():
    """Create an authorized gspread client from the service account file."""
    credentials = Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=SCOPES,
    )
    return gspread.authorize(credentials)


def save_daily_record(record):
    """
    Persist one daily record.

    Expected keys: date, weight, skinfolds_sum, bmr, cml
    (no GUI knowledge, no business-rule knowledge)
    """
    row = _record_to_sheet_row(record)
    client = create_gspread_client()

    try:
        spreadsheet = client.open(SHEET_NAME)
    except SpreadsheetNotFound as error:
        raise RuntimeError(
            f'Spreadsheet "{SHEET_NAME}" was not found.\n'
            "Check SHEET_NAME in repository.py and share the sheet "
            "with the service account email."
        ) from error

    worksheet = spreadsheet.sheet1
    try:
        # RAW keeps values as text (left-aligned like older rows)
        worksheet.append_row(row, value_input_option="RAW")
    except APIError as error:
        if _is_empty_success_response(error):
            return record
        raise RuntimeError(_describe_error(error)) from error
    except Exception as error:
        if _is_empty_success_response(error):
            return record
        raise RuntimeError(_describe_error(error)) from error

    return record


def _format_float(value):
    """Format numbers like the existing sheet table (e.g. 65.0, 1887.6)."""
    return f"{float(value):.1f}"


def _record_to_sheet_row(record):
    """Turn a plain daily record dict into one Google Sheets row."""
    return [
        record["date"],
        _format_float(record["weight"]),
        _format_float(record["skinfolds_sum"]),
        _format_float(record["bmr"]),
        _format_float(record["cml"]),
    ]


def _get_http_response(error):
    response = getattr(error, "response", None)
    if response is not None:
        return response
    if getattr(error, "args", None):
        first = error.args[0]
        if hasattr(first, "status_code"):
            return first
    return None


def _is_empty_success_response(error):
    # gspread can raise on HTTP 200 when the success body is empty
    response = _get_http_response(error)
    return getattr(response, "status_code", None) == 200


def _describe_error(error):
    response = _get_http_response(error)
    if response is not None:
        status = getattr(response, "status_code", "?")
        body = (getattr(response, "text", "") or "").strip()
        if not body:
            body = "(no details returned by Google)"
        return f"{type(error).__name__} (HTTP {status})\n{body[:400]}"
    return f"{type(error).__name__}: {error}"
