# scripts/data.py
import random

vendors = [
    "Siemens", "ABB", "Honeywell", "Schneider Electric", "GE", "Emerson"
]

equipment = [
    "Pump", "Compressor", "Boiler", "Chiller", "Turbine", "Generator"
]

projects = [
    "Alpha Refinery", "Beta Solar Plant", "Gamma Wind Farm",
    "Delta Chemical Plant", "Epsilon Data Center"
]

statuses = ["Open", "Closed", "Pending", "Approved", "Rejected"]

def random_vendor():
    return random.choice(vendors)

def random_equipment():
    return random.choice(equipment)

def random_project():
    return random.choice(projects)

def random_status():
    return random.choice(statuses)

def random_date():
    year = random.choice([2024, 2025, 2026])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"
