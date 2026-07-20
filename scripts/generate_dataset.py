# scripts/generate_dataset.py
from pdf_generator import generate_all_pdfs
from csv_generator import generate_all_csvs

def main():
    print("Generating PDFs...")
    generate_all_pdfs()

    print("Generating CSVs...")
    generate_all_csvs()

    print("Dataset generation completed!")

if __name__ == "__main__":
    main()
