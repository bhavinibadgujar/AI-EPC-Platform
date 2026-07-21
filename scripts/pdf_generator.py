from fpdf import FPDF
import random

from data import (
    random_project,
    random_vendor,
    random_equipment,
    random_date,
)

from utils import get_output_path
from epc_sections import generate_section, SECTIONS


class EPCPDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "AI EPC Platform - Engineering Specification", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def create_specification(filename):

    pdf = EPCPDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(0, 10, "Engineering Specification", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    pdf.cell(0, 8, f"Project : {random_project()}", ln=True)
    pdf.cell(0, 8, f"Vendor  : {random_vendor()}", ln=True)
    pdf.cell(0, 8, f"Equipment : {random_equipment()}", ln=True)
    pdf.cell(0, 8, f"Issue Date : {random_date()}", ln=True)

    pdf.ln(10)

    # Generate all sections
    for section_name in SECTIONS.keys():

        pdf.set_font("Arial", "B", 14)

        pdf.multi_cell(0, 8, section_name)

        pdf.ln(2)

        pdf.set_font("Arial", size=11)

        paragraphs = generate_section(
            section_name,
            paragraphs=35
        )

        for paragraph in paragraphs:

            pdf.multi_cell(0, 7, paragraph)

            pdf.ln(1)

        pdf.ln(5)

    output = get_output_path("output/pdfs", filename)

    pdf.output(output)

    print(f"Generated {output}")


def generate_specifications(count=5):

    for i in range(count):

        create_specification(
            f"spec_{i+1}.pdf"
        )


if __name__ == "__main__":

    generate_specifications()