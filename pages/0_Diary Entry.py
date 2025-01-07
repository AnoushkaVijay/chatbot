import streamlit as st
from fpdf import FPDF
import datetime

def create_pdf(diary_text, date):
    """Creates a PDF with the diary entry."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Diary Entry - {date}", ln=True, align='C')
    pdf.ln(10)  # Line break

    # Add the diary text
    for line in diary_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    return pdf

def main():
    st.title("Diary Entry")

    # Text area for the diary entry
    diary_text = st.text_area("Write your diary entry below:", height=300)

    # Button to download the diary as a PDF
    if st.button("Download as PDF"):
        if diary_text.strip():
            # Generate the PDF
            date = datetime.date.today().strftime("%Y-%m-%d")
            pdf = create_pdf(diary_text, date)

            # Stream the PDF as a downloadable file
            pdf_output = pdf.output(dest="S").encode("latin1")
            st.download_button(
                label="Click here to download your PDF",
                data=pdf_output,
                file_name=f"Diary_Entry_{date}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please write something in the diary before downloading.")

if __name__ == "__main__":
    main()
