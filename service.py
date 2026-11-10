# -----------------------------
# 1. IMPORTS
# -----------------------------
# from random import randint, randrange
from datetime import date

from repository import save_daily_record

# -----------------------------
# 2. SETUP (CONSTANTS & LISTS & DICTIONARIES)
# -----------------------------
# always 1.2 - we are calculating CML without any daily exercise
TODAYS_ACT_FACTOR = 1.2
TITLES = {
    "Female": "dear Madam",
    "Male": "dear Sir",
}

# Using a List of Dictionaries to store complete user profiles
users = [
    {
        "name": "Anna",
        "weight": 65.0,
        "reference": "dear Madam",
        "skinfolds_sum": 55,
        "age_in_years": 47,
    },
    {
        "name": "John",
        "weight": 82.5,
        "reference": "dear Sir",
        "skinfolds_sum": 45,
        "age_in_years": 55,
    },
    {
        "name": "Sasha",
        "weight": 70.0,
        "reference": "dear Madam",
        "skinfolds_sum": 50,
        "age_in_years": 30,
    },
]

# -----------------------------
# 3. FUNCTIONS
# -----------------------------
def calc_user_cml(user_weight, user_act_factor):
    bmr = user_weight * 24.2  # Basal Metabolic Rate (in kcal/day)
    return round(bmr * user_act_factor, 2)  # Calorie Maintenance Level (in kcal/day)


def calc_user_bmr(user_weight):
    return round(user_weight * 24.2, 2)


def calc_user_fat_perc(skinfolds_sum, age_in_years, reference):
    if reference == TITLES["Male"]:
        body_density = (
            1.10938
            - (0.0008267 * skinfolds_sum)
            + (0.0000016 * (skinfolds_sum ** 2))
            - (0.0002574 * age_in_years)
        )
    elif reference == TITLES["Female"]:
        body_density = (
            1.0994921
            - (0.0009929 * skinfolds_sum)
            + (0.0000023 * (skinfolds_sum ** 2))
            - (0.0001392 * age_in_years)
        )
    return round((495 / body_density) - 450, 2)  # Current Body Fat Percentage (in %)


def calc_user_fat_lvl(user_weight, fat_perc):
    return round(user_weight / 100 * fat_perc, 2)  # Current Body Fat Level (in kg)


def input_weight_fail_proof():
    while True:
        try:
            # Check if the user input for the 'weight' variable is the correct data type
            user_weight = float(input("\nWhat is your current weight? "))
            print("\nThank you.")
            return user_weight
        except ValueError:
            # If an error occurs (like typing text instead of a float)
            print("You need to type a whole or decimal number. Try again.")


def input_sex_fail_proof():
    while True:
        # .strip() removes accidental spaces, .title() capitalizes the first letter
        sex = input("What is your sex? (Male/Female) ").strip().title()
        # Check if the user input is correct
        if sex in TITLES:
            return TITLES[sex]
        print("You need to type 'Male' or 'Female'. Try again.")


def input_whole_number_fail_proof(prompt_text):
    while True:
        try:
            return int(input(prompt_text))
        except ValueError:
            print("You need to type a whole or decimal number. Try again.")

# GUI / layered-app helpers
def build_todays_record(user):
    """Build a plain daily record (no database details)."""
    return {
        "date": todays_date_str(),
        "weight": user["weight"],
        "skinfolds_sum": user["skinfolds_sum"],
        "bmr": calc_user_bmr(user["weight"]),
        "cml": calc_user_cml(user["weight"], TODAYS_ACT_FACTOR),
    }

def todays_date_str():
    """Build a string representation of the current date."""
    return date.today().strftime("%d-%m-%Y")


def save_todays_user_record(user):
    """Service API: calculate today's record, then ask the repository to save it."""
    record = build_todays_record(user)
    save_daily_record(record)
    return record

def build_user_stats_message(user):
    fat_perc = calc_user_fat_perc(
        user["skinfolds_sum"],
        user["age_in_years"],
        user["reference"],
    )
    fat_kg = calc_user_fat_lvl(user["weight"], fat_perc)
    cml = calc_user_cml(user["weight"], TODAYS_ACT_FACTOR)
    return (
        f"\nWithout any exercise at all, {user['reference']},"
        f"\nyou could consume up to {cml}kcal today"
        "\nto preserve your current weight."
        "\n\nYour current fat balance is:"
        f"\n{fat_kg}kg fat ({fat_perc}% of your body weight)\n"
    )

def get_user_names():
    return [user["name"] for user in users]

def find_user_by_name(user_name):
    for user in users:
        if user["name"] == user_name:
            return user
    return None

def add_user(name, weight, reference, skinfolds_sum, age_in_years):
    user = {
        "name": name,
        "weight": weight,
        "reference": reference,
        "skinfolds_sum": skinfolds_sum,
        "age_in_years": age_in_years,
    }
    users.append(user)
    return user


# -----------------------------
# 4. MAIN PROGRAM (console version - barred for GUI app)
# -----------------------------
"""
no longer here, moved to main.py
"""
