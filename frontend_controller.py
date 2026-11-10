# -----------------------------
# 1. IMPORTS
# -----------------------------
from pathlib import Path

from guizero import App, Box, ButtonGroup, Combo, Picture, PushButton, Text, TextBox

from service import (
    TITLES,
    add_user,
    build_user_stats_message,
    find_user_by_name,
    get_user_names,
    save_todays_user_record,
)

# -----------------------------
# 2. SETUP (CONSTANTS & DICTIONARIES)
# -----------------------------
IMAGE_PATH = str(Path(__file__).resolve().parent / "images" / "pic2.png")
LABEL_WIDTH = 20
FIELD_WIDTH = 28
BUTTON_WIDTH = 32
MODE_EXISTING = "Existing user"
MODE_REGISTER = "Register a new user"

# -----------------------------
# 3. FUNCTIONS
# -----------------------------
def show_selected_section():
    if mode_group.value == MODE_EXISTING:
        user_card.show()
        register_card.hide()
    else:
        register_card.show()
        user_card.hide()


def refresh_user_combo(selected_name):
    user_combo.clear()
    for name in get_user_names():
        user_combo.append(name)
    user_combo.value = selected_name


def set_status(message):
    status_box.value = message


def set_stats(message):
    stats_box.value = message


def register_user():
    name = name_box.value.strip()
    if not name:
        set_status("Name is required.")
        return
    if find_user_by_name(name) is not None:
        set_status(f"User '{name}' already exists.")
        return

    try:
        weight = float(weight_box.value)
        skinfolds_sum = int(skinfolds_box.value)
        age_in_years = int(age_box.value)
    except ValueError:
        set_status("You need to type a whole or decimal number. Try again.")
        return

    add_user(name, weight, TITLES[sex_box.value], skinfolds_sum, age_in_years)
    refresh_user_combo(name)
    clear_register_fields()

    mode_group.value = MODE_EXISTING
    show_selected_section()
    set_status(f"User {name} has been added.")


def show_selected_user_stats():
    name = user_combo.value
    user = find_user_by_name(name)
    set_stats(build_user_stats_message(user).strip())
    set_status(f"Showing stats for {name}.")


def save_selected_user_to_sheet():
    name = user_combo.value
    user = find_user_by_name(name)
    try:
        save_todays_user_record(user)
        set_status(f"Saved today's data for {name}.")
    except FileNotFoundError:
        set_status(
            "Could not save: storage credentials file is missing.\n"
            "Check SERVICE_ACCOUNT_FILE in repository.py."
        )
    except Exception as error:
        set_status(f"Could not save:\n{error}")


def clear_register_fields():
    name_box.value = ""
    weight_box.value = ""
    sex_box.value = "Female"
    skinfolds_box.value = ""
    age_box.value = ""


def run():
    app.display()


# -----------------------------
# 4. MAIN PROGRAM
# -----------------------------
app = App(title="Fat Burner", width=460, height=860, bg="#dfe7f1")

header = Box(app, width="fill", border=True, align="top")
header.bg = "#ffffff"
Text(header, text="Fat Burner", size=26, color="#1a1a1a")
Picture(header, image=IMAGE_PATH, width=100, height=100)
Text(
    header,
    text="Track users, fat estimates, and calorie maintenance.",
    size=10,
    color="#555555",
)

mode_card = Box(app, width="fill", border=True, align="top")
mode_card.bg = "#ffffff"
Text(mode_card, text="Choose a section", size=12, color="#333333")
mode_group = ButtonGroup(
    mode_card,
    options=[MODE_EXISTING, MODE_REGISTER],
    selected=MODE_EXISTING,
    command=show_selected_section,
)

content = Box(app, width="fill", align="top")

user_card = Box(content, width="fill", border=True, align="top")
user_card.bg = "#ffffff"
Text(user_card, text="Existing user", size=15, color="#1a1a1a")
Text(user_card, text="Choose user", size=11, color="#333333")
user_combo = Combo(
    user_card,
    options=get_user_names(),
    width=FIELD_WIDTH,
    selected=get_user_names()[0],
)
PushButton(
    user_card,
    command=show_selected_user_stats,
    text="Show my stats",
    width=BUTTON_WIDTH,
)
PushButton(
    user_card,
    command=save_selected_user_to_sheet,
    text="Save today to Google Sheets",
    width=BUTTON_WIDTH,
)
Text(user_card, text="Stats", size=11, color="#333333")
stats_box = TextBox(
    user_card,
    text="No stats yet.",
    width=48,
    height=6,
    multiline=True,
    scrollbar=True,
)
stats_box.bg = "#f5f5f5"

register_card = Box(content, width="fill", border=True, align="top")
register_card.bg = "#ffffff"
Text(register_card, text="Register a new user", size=15, color="#1a1a1a")

form = Box(register_card, layout="grid", width="fill", align="top")
Text(form, text="Name", width=LABEL_WIDTH, grid=[0, 0], align="left")
name_box = TextBox(form, width=FIELD_WIDTH, grid=[1, 0], align="left")
Text(form, text="Weight (kg)", width=LABEL_WIDTH, grid=[0, 1], align="left")
weight_box = TextBox(form, width=FIELD_WIDTH, grid=[1, 1], align="left")
Text(form, text="Sex", width=LABEL_WIDTH, grid=[0, 2], align="left")
sex_box = Combo(
    form,
    options=["Female", "Male"],
    selected="Female",
    width=FIELD_WIDTH,
    grid=[1, 2],
    align="left",
)
Text(form, text="Skinfolds (mm)", width=LABEL_WIDTH, grid=[0, 3], align="left")
skinfolds_box = TextBox(form, width=FIELD_WIDTH, grid=[1, 3], align="left")
Text(form, text="Age (years)", width=LABEL_WIDTH, grid=[0, 4], align="left")
age_box = TextBox(form, width=FIELD_WIDTH, grid=[1, 4], align="left")

PushButton(
    register_card,
    command=register_user,
    text="Register user",
    width=BUTTON_WIDTH,
)

status_card = Box(app, width="fill", border=True, align="top")
status_card.bg = "#ffffff"
Text(status_card, text="Status", size=11, color="#333333")
status_box = TextBox(
    status_card,
    text="Choose a section, then use the form above.",
    width=48,
    height=4,
    multiline=True,
    scrollbar=True,
)
status_box.bg = "#f5f5f5"

register_card.hide()
