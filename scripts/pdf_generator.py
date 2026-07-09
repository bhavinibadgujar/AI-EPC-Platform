# scripts/pdf_generator.py
from fpdf import FPDF
import random
from data import random_vendor, random_equipment, random_project, random_status, random_date
from utils import get_output_path

def create_pdf(title: str, content: list, filename: str, folder: str = "output/pdfs"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    for line in content:
        pdf.multi_cell(0, 10, line)

    output_path = get_output_path(folder, filename)
    pdf.output(output_path)
    print(f"Generated: {output_path}")

# --- Generators for each type of EPC document ---

def generate_specifications(count=10):
    for i in range(count):
        content = [
            f"Project: {random_project()}",
            f"Equipment: {random_equipment()}",
            f"Vendor: {random_vendor()}",
            f"Date: {random_date()}",
            "Specification details go here..."
        ]
        create_pdf("Specification", content, f"spec_{i+1}.pdf")

def generate_vendor_submittals(count=10):
    for i in range(count):
        content = [
            f"Vendor: {random_vendor()}",
            f"Equipment: {random_equipment()}",
            f"Project: {random_project()}",
            f"Status: {random_status()}",
            f"Date: {random_date()}",
            "Vendor submittal details..."
        ]
        create_pdf("Vendor Submittal", content, f"vendor_submittal_{i+1}.pdf")

def generate_rfis(count=20):
    for i in range(count):
        content = [
            f"Project: {random_project()}",
            f"RFI Number: {i+1}",
            f"Status: {random_status()}",
            f"Date: {random_date()}",
            "Request for Information details..."
        ]
        create_pdf("RFI", content, f"rfi_{i+1}.pdf")

def generate_meeting_minutes(count=20):
    for i in range(count):
        content = [
            f"Project: {random_project()}",
            f"Meeting Date: {random_date()}",
            f"Attendees: {random_vendor()}, {random_vendor()}",
            "Discussion points...",
            "Action items..."
        ]
        create_pdf("Meeting Minutes", content, f"meeting_minutes_{i+1}.pdf")

def generate_commissioning_checklists(count=10):
    for i in range(count):
        content = [
            f"Project: {random_project()}",
            f"Equipment: {random_equipment()}",
            f"Date: {random_date()}",
            "Commissioning checklist items..."
        ]
        create_pdf("Commissioning Checklist", content, f"commissioning_{i+1}.pdf")

# --- Master function ---
def generate_all_pdfs():
    generate_specifications()
    generate_vendor_submittals()
    generate_rfis()
    generate_meeting_minutes()
    generate_commissioning_checklists()
