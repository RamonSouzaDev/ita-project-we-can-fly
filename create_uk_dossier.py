import os
import sys

# Ensure packages are installed or handle errors gracefully
try:
    from fpdf import FPDF
    from PyPDF2 import PdfMerger
except ImportError:
    print("Required libraries missing. Please run: pip install PyPDF2 fpdf")
    sys.exit(1)

text_intro = """
Professional Dossier & Project Presentation
Applicant: Ramon de Souza Mendes
Target: UK Engineering Council / Licensed Institutions (IET / BCS)

This dossier contains:
1. Presentation of the "We Can Fly" Engineering Project.
2. CREA-SP Certificate for Reciprocity (Mutual Recognition).
3. Curriculum Vitae (CV) - Ramon de Souza Mendes.

---
WE CAN FLY - AERONAUTIC CYBERSECURITY & AI PROJECT

"We Can Fly" is an innovative, mature software engineering project (TRL-9) created by Ramon de Souza Mendes, demonstrating advanced capabilities in critical systems development.

Key Project Highlights:
- Domain: Aeronautic Cybersecurity and Artificial Intelligence.
- Objective: Implements robust threat detection mechanisms for ADS-B and ARINC 429 aviation protocols, assuring safe communications.
- Regulatory Compliance: Adheres to DECEA 2030, LGPD, and ISO 27001 standards.
- Official Registry: Registered with the Brazilian Regional Council of Engineering and Agronomy (CREA-SP) under ART LC39711825-2620260207668.
- Technology Stack: Integrates advanced Python, Google Cloud Platform (GCP), GitHub CI/CD, and machine learning models for anomaly detection.

This project showcases the applicant's ability to lead complex software architecture design, implement mission-critical security, and operate at the highest standards of international engineering practices.
"""

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Applicant Dossier - Ramon de Souza Mendes', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_intro_pdf(filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    
    for line in text_intro.split('\n'):
        # using multi_cell to handle wrapping
        pdf.multi_cell(0, 7, line)
        
    pdf.output(filename, 'F')
    print(f"Created {filename}")

def build_dossier():
    base_dir = r"c:\Users\dwmom\OneDrive\Documentos"
    intro_pdf = os.path.join(base_dir, "this-week-23-03-26", "00_Intro_We_Can_Fly.pdf")
    
    create_intro_pdf(intro_pdf)
    
    docs = [
        intro_pdf,
        os.path.join(base_dir, "Certidão nº 055-2026 - Ramon de Souza Mendes.pdf"),
        os.path.join(base_dir, "gemini-3.1-we-can-fly", "documentos_contabeis", "Curriculo.pdf")
    ]
    
    output_pdf = os.path.join(base_dir, "this-week-23-03-26", "UK_Engineering_Council_Dossier.pdf")
    
    merger = PdfMerger()
    merged_count = 0
    for doc in docs:
        if os.path.exists(doc):
            try:
                merger.append(doc)
                print(f"Successfully appended: {os.path.basename(doc)}")
                merged_count += 1
            except Exception as e:
                print(f"Failed to append {doc}: {e}")
        else:
            print(f"Document not found (skipping): {doc}")
            
    if merged_count > 0:
        merger.write(output_pdf)
        merger.close()
        print(f"\nDossier successfully created at: {output_pdf}")
    else:
        print("No documents were merged.")

if __name__ == "__main__":
    build_dossier()
