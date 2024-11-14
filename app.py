import fitz  # PyMuPDF
import os
import streamlit as st
import zipfile

# Function to split PDF based on user-defined page numbers
def split_pdf_by_pages(pdf, page_counts, output_folder):
    document = fitz.open(stream=pdf.read(), filetype="pdf")
    output_files = []
    start_page = 0

    for idx, count in enumerate(page_counts):
        end_page = start_page + count - 1
        output_pdf = fitz.open()  # Create a new PDF document
        output_pdf.insert_pdf(document, from_page=start_page, to_page=end_page)
        
        # Save the split PDF
        doc_name = os.path.join(output_folder, f"document_{idx + 1}.pdf")
        output_pdf.save(doc_name)
        output_files.append(doc_name)
        output_pdf.close()
        
        # Update start page for the next segment
        start_page = end_page + 1

    return output_files

# Streamlit Interface
st.title("PDF Splitter by Page Counts - by: Samir Hettawy")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Display instructions
    st.write("Enter the number of pages for each split separated by commas (e.g., 2, 3, 5, 10...)")
    
    # User input for split configuration
    page_counts_input = st.text_input("Page Counts")
    
    if page_counts_input:
        # Convert input to a list of integers
        page_counts = [int(x.strip()) for x in page_counts_input.split(",") if x.strip().isdigit()]
        total_pages = sum(page_counts)

        # Load the document and check if total pages match
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        if total_pages != document.page_count:
            st.error(f"Total pages in the split ({total_pages}) does not match the document's total pages ({document.page_count}). Please adjust the counts.")
        else:
            # Create output folder
            output_folder = "E:\\الملفات_المقسمة"
            os.makedirs(output_folder, exist_ok=True)

            # Split PDF based on user-defined page counts
            output_files = split_pdf_by_pages(uploaded_file, page_counts, output_folder)

            # Create a ZIP file to compress the output files
            zip_filename = os.path.join(output_folder, uploaded_file.name.replace(".pdf", ".zip"))
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in output_files:
                    zipf.write(file, os.path.basename(file))

            # Delete individual PDF files after adding them to ZIP
            for file in output_files:
                os.remove(file)

            # Provide download button for the ZIP file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download All as ZIP",
                    data=f,
                    file_name=os.path.basename(zip_filename),
                    mime="application/zip"
                )

            st.success("PDF splitting and ZIP compression completed successfully!")
