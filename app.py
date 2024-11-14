import fitz  # PyMuPDF
import os
import streamlit as st
import zipfile

# Function to split PDF into individual pages
def split_pdf_individual_pages(pdf_data, output_folder):
    document = fitz.open(stream=pdf_data, filetype="pdf")
    output_files = []

    for page_number in range(len(document)):
        output_pdf = fitz.open()  # Create a new PDF document
        output_pdf.insert_pdf(document, from_page=page_number, to_page=page_number)

        # Save each page as a separate PDF
        doc_name = os.path.join(output_folder, f"document_{page_number + 1}.pdf")
        output_pdf.save(doc_name)
        output_files.append(doc_name)
        output_pdf.close()

    return output_files

# Function to split PDF based on custom ranges
def split_pdf_custom_ranges(pdf_data, ranges, output_folder):
    document = fitz.open(stream=pdf_data, filetype="pdf")
    output_files = []

    for idx, (start_page, end_page) in enumerate(ranges):
        output_pdf = fitz.open()  # Create a new PDF document
        output_pdf.insert_pdf(document, from_page=start_page, to_page=end_page)

        # Save the split PDF
        doc_name = os.path.join(output_folder, f"document_{idx + 1}.pdf")
        output_pdf.save(doc_name)
        output_files.append(doc_name)
        output_pdf.close()

    return output_files

# Streamlit Interface
st.set_page_config(page_title="تقسيم ملفات PDF - برمجة: المستشار سمير عبد العظيم حيطاوي", layout="centered")

# Set styles for the app
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F8FF;
    }
    .stTitle, .stHeader {
        color: #B22222;
    }
    .instruction {
        font-size: large;
        color: #000080;
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #000000;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        color: #B22222;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titles
st.markdown("<div class='main-title'>تقسيم ملفات PDF</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title' style='font-size: 10px;'>برمجة: المستشار سمير عبد العظيم حيطاوي</div>", unsafe_allow_html=True)

# Display usage instructions
st.markdown("<h3 style='text-align: center;'>تعليمات الاستخدام</h3>>
<div class='instruction'>ارفع الملف ثم اختر طريقة التقسيم المناسبة لك: تقسيم كل ورقة في ملف منفصل أو تقسيم إلى ملفات تحتوي على نطاق من الصفحات.</div>", unsafe_allow_html=True)

# Upload PDF file
uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read file data
    pdf_data = uploaded_file.read()
    document = fitz.open(stream=pdf_data, filetype="pdf")
    
    # Option selection
    split_option = st.radio("اختر طريقة التقسيم:", ("تقسيم المستند إلى ملفات فردية (كل ورقة على حدة)", "تقسيم المستند إلى ملفات متعددة تحتوي على أكثر من ورقة"))
    
    if split_option == "تقسيم المستند إلى ملفات فردية (كل ورقة على حدة)":
        # Split each page into a separate PDF
        st.write("سيتم تقسيم المستند إلى ملفات فردية، كل ملف يحتوي على ورقة واحدة.")
        
        # Create output folder
        output_folder = "E:\\الملفات_المقسمة"
        os.makedirs(output_folder, exist_ok=True)

        # Split and save files
        output_files = split_pdf_individual_pages(pdf_data, output_folder)

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
    if st.button('تحويل الآن'):
        st.download_button(
            label="تحميل الكل كملف ZIP",
            data=f,
            file_name=os.path.basename(zip_filename),
            mime="application/zip"
        )
            )

        st.success("تم تقسيم الملفات بنجاح وتحويلها إلى ملف مضغوط!")

            st.button('رفع ملف جديد', on_click=lambda: st.experimental_rerun())

    elif split_option == "تقسيم المستند إلى ملفات متعددة تحتوي على أكثر من ورقة":
        st.write("أدخل تفاصيل تقسيم الملف، مثال: الملف الأول من صفحة 1 إلى 4، الملف الثاني من صفحة 5 إلى 20.")
        
        # User input for custom page ranges
        page_ranges_input = import pandas as pd

page_ranges_df = st.experimental_data_editor(
    pd.DataFrame(columns=['اسم الملف (اختياري)', 'من صفحة (إجباري)', 'إلى صفحة (إجباري)']),
    use_container_width=True,
    num_rows='dynamic'
)', 'من صفحة (إجباري)', 'إلى صفحة (إجباري)']),
            use_container_width=True,
            num_rows='dynamic'
        )
        
        if not page_ranges_df.empty:
            try:
                # Parse input to extract ranges
                ranges = []
                for idx, row in page_ranges_df.iterrows():
                    if pd.notna(row['من صفحة (إجباري)']) and pd.notna(row['إلى صفحة (إجباري)']):
    start_page = int(row['من صفحة (إجباري)']) - 1
    end_page = int(row['إلى صفحة (إجباري)']) - 1
    if start_page < 0 or end_page >= len(document) or start_page > end_page:
        st.error(f"المدى المدخل غير صالح: من صفحة {row['من صفحة (إجباري)']} إلى صفحة {row['إلى صفحة (إجباري)']}")
        break
    ranges.append((start_page, end_page))
                
                if ranges:
                    # Create output folder
                    output_folder = "E:\\الملفات_المقسمة"
                    os.makedirs(output_folder, exist_ok=True)

                    # Split PDF based on custom ranges
                    output_files = split_pdf_custom_ranges(pdf_data, ranges, output_folder)

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
                            label="تحميل الكل كملف ZIP",
                            data=f,
                            file_name=os.path.basename(zip_filename),
                            mime="application/zip"
                        )

                    st.success("تم تقسيم الملفات بنجاح وتحويلها إلى ملف مضغوط!")

            except ValueError:
                st.error("الرجاء التأكد من صحة التنسيق المدخل.")
