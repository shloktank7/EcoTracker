#!/usr/bin/env python3
# EcoTracker: Track your daily carbon footprint in plain English

import json
import os
import datetime
import random

# Emission factors
CAR_CO2_PER_MILE = 0.411
TRANSIT_CO2_PER_MILE = 0.089
ELEC_CO2_PER_KWH = 0.42

# Diet options: (label, kg CO2 per day)
DIET_CO2 = {
    "1": ("Omnivore", 5.0),
    "2": ("Vegetarian", 3.5),
    "3": ("Vegan", 2.5),
}

DATA_FILE = "ecotracker_data.json"

QUOTES = [
    "Small steps can lead to huge impacts.",
    "Change starts with you!",
    "Every day is a new chance to reduce your footprint.",
    "Be the reason the planet smiles.",
    "Living green is living smart.",
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except Exception:
        print("Couldn't load saved data — starting fresh.")
        return []

def save_data(entries):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(entries, f, indent=2)
    except Exception as e:
        print("Error saving data:", e)

def calc_emissions(entry):
    car = entry["car_miles"] * CAR_CO2_PER_MILE
    transit = entry["transit_miles"] * TRANSIT_CO2_PER_MILE
    elec = entry["elec_kwh"] * ELEC_CO2_PER_KWH
    diet = DIET_CO2[entry["diet"]][1]
    total = car + transit + elec + diet
    return {"car": car, "transit": transit, "elec": elec, "diet": diet, "total": total}

def add_entry():
    print("\nTell me about your day:")
    today = datetime.date.today().isoformat()
    date = input(f"Date (YYYY‑MM‑DD) [default {today}]: ").strip() or today
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Oops, wrong date format. Try YYYY‑MM‑DD.")
        return

    try:
        car_miles = float(input("How many miles did you drive today? ").strip())
    except ValueError:
        print("That doesn't look like a number.")
        return

    try:
        transit_miles = float(input("Miles on bus/train today? ").strip())
    except ValueError:
        print("That doesn't look like a number.")
        return

    print("How was your electricity use today?")
    print("  1) Light (~10 kWh)")
    print("  2) Moderate (~25 kWh)")
    print("  3) Heavy (~40 kWh)")
    elec_choice = input("Pick 1, 2, or 3: ").strip()
    mapping = {"1": 10.0, "2": 25.0, "3": 40.0}
    if elec_choice not in mapping:
        print("Invalid choice.")
        return
    elec_kwh = mapping[elec_choice]

    print("What’s your diet like?")
    print("  1) Omnivore")
    print("  2) Vegetarian")
    print("  3) Vegan")
    diet = input("Pick 1, 2, or 3: ").strip()
    if diet not in DIET_CO2:
        print("Invalid choice.")
        return

    entry = {
        "date": date,
        "car_miles": car_miles,
        "transit_miles": transit_miles,
        "elec_kwh": elec_kwh,
        "diet": diet
    }
    entry["emissions"] = calc_emissions(entry)

    data = load_data()
    data.append(entry)
    save_data(data)

    print(f"\nGreat! On {date}, your total CO₂ was {entry['emissions']['total']:.2f} kg\n")

def show_report():
    data = load_data()
    if not data:
        print("\nNo entries yet. Try adding one first!\n")
        return

    print("\n--- Your Carbon Footprint Report ---")
    grand_total = 0
    for e in data:
        em = e["emissions"]
        diet_label = DIET_CO2[e["diet"]][0]
        print(f"\nDate: {e['date']}")
        print(f"  Car:        {em['car']:.2f} kg")
        print(f"  Transit:    {em['transit']:.2f} kg")
        print(f"  Electricity:{em['elec']:.2f} kg")
        print(f"  Diet ({diet_label}): {em['diet']:.2f} kg")
        print(f"  Total:      {em['total']:.2f} kg")
        grand_total += em["total"]

    avg = grand_total / len(data)
    print(f"\nEntries: {len(data)}   Total CO₂: {grand_total:.2f} kg   Avg/day: {avg:.2f} kg\n")

def give_tips():
    data = load_data()
    if not data:
        print("\nNo data to give tips on — add an entry first!\n")
        return

    e = data[-1]
    tips = []
    if e["car_miles"] > 20:
        tips.append("Try carpooling or grouping errands together.")
    if e["transit_miles"] < 5:
        tips.append("Could you swap a drive for the bus or train?")
    if e["elec_kwh"] > 30:
        tips.append("Turn off unused lights/appliances.")
    if e["diet"] == "1":
        tips.append("Maybe try a meatless meal now and then.")

    if not tips:
        tips = ["Nice work! Keep up the eco-friendly habits."]

    print("\n--- Green Tips Based on Your Last Entry ---")
    for t in tips:
        print(" •", t)
    print()

def show_quote():
    print("\n“" + random.choice(QUOTES) + "”\n")

def main_menu():
    while True:
        print("EcoTracker Menu:")
        print(" 1) Add today’s entry")
        print(" 2) Show my report")
        print(" 3) Get tips from my last entry")
        print(" 4) Random motivational quote")
        print(" 5) Exit")
        choice = input("Your choice? ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            show_report()
        elif choice == "3":
            give_tips()
        elif choice == "4":
            show_quote()
        elif choice == "5":
            print("\nThanks for using EcoTracker—stay green!\n")
            break
        else:
            print("Pick a number between 1 and 5.\n")

if __name__ == "__main__":
    main_menu()
