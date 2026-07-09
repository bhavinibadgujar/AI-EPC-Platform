# scripts/csv_generator.py
import csv
from data import random_vendor, random_equipment, random_project, random_status, random_date
from utils import get_output_path

def create_csv(headers: list, rows: list, filename: str, folder: str = "output/csvs"):
    output_path = get_output_path(folder, filename)
    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated: {output_path}")

# --- Generators for EPC CSVs ---

def generate_schedule_csv(count=20):
    headers = ["Project", "Equipment", "Planned Date", "Status"]
    rows = []
    for _ in range(count):
        rows.append([
            random_project(),
            random_equipment(),
            random_date(),
            random_status()
        ])
    create_csv(headers, rows, "schedule.csv")

def generate_procurement_csv(count=20):
    headers = ["Vendor", "Equipment", "Project", "Status", "Date"]
    rows = []
    for _ in range(count):
        rows.append([
            random_vendor(),
            random_equipment(),
            random_project(),
            random_status(),
            random_date()
        ])
    create_csv(headers, rows, "procurement.csv")

# --- Master function ---
def generate_all_csvs():
    generate_schedule_csv()
    generate_procurement_csv()
