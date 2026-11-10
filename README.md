# Fat Burner App (pre-OOP mini app)

Desktop app that tracks weight / skinfold-based fat estimates and calorie
maintenance level, then optionally saves today's row to storage.

Simple clean-architecture split (plug/unplug each layer):

| Layer | File | Knows about |
|---|---|---|
| Controller (frontend) | `gui.py` | widgets only; calls `logic` |
| Service (backend) | `logic.py` | users, calcs; calls `repository` |
| Repository (DB) | `repository.py` | storage settings + Google Sheets details |
| Entry | `main.py` | starts the app |

Swap the GUI framework → change `gui.py` only.  
Swap Sheets for SQLite/CSV → change `repository.py` only.

## Learning pathway

1. `logic.py` — continuous from the console lesson  
   (`# 2. SETUP (CONSTANTS & DICTIONARIES)`, calc + `input_*_fail_proof`)
2. `repository.py` — persistence settings + Google Sheets save
3. `gui.py` — thin frontend / controller
4. `main.py` — entry point (`python main.py`)

## Features

- Register multiple users (in-memory list of dictionaries)
- Select a user and view CML + estimated body-fat stats
- Save today's date / weight / skinfolds / BMR / CML via the repository

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

1. Place your Google service account JSON next to `repository.py`
2. Set `SERVICE_ACCOUNT_FILE` / `SHEET_NAME` in `repository.py`
3. Share the sheet with the service account email

## Run

```bash
python main.py
```

Next course step: turn service/repository functions into objects (OOP),
keeping the GUI humble.
