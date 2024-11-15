import fitz  # PyMuPDF
import os
import streamlit as st
import zipfile

# Function to split PDF based on custom ranges
def split_pdf_custom_ranges(pdf_data, ranges, output_folder):
    document = fitz.open(stream=pdf_data, filetype="pdf")
    output_files = []

    for idx, (start_page, end_page, doc_name) in enumerate(ranges):
        output_pdf = fitz.open()  # Create a new PDF document
        output_pdf.insert_pdf(document, from_page=start_page, to_page=end_page)

        # Save the split PDF
        doc_name = os.path.join(output_folder, f"{doc_name}.pdf" if doc_name else f"document_{idx + 1}.pdf")
        output_pdf.save(doc_name)
        output_files.append(doc_name)
        output_pdf.close()

    return output_files

# Streamlit Interface
st.set_page_config(page_title="تقسيم ملفات PDF - تصميم: المستشار سمير عبد العظيم حيطاوي", layout="centered")

# Set styles for the app
st.markdown(
    """
    <style>
    .stApp {
        /* Remove the custom background color to support dark mode */
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
st.markdown("<div class='sub-title' style='font-size: 10px;'>تصميم: المستشار سمير عبد العظيم حيطاوي</div>", unsafe_allow_html=True)

# Display usage instructions
st.markdown("<h3 style='text-align: center;'>تعليمات الاستخدام</h3>", unsafe_allow_html=True)
st.markdown("<div class='instruction'>ارفع الملف ثم اختر طريقة التقسيم المناسبة لك من خلال إدخال المستندات. يجب أن تُحدد نطاق كل مستند بإدخال الصفحات من وإلى. </div>", unsafe_allow_html=True)

# Upload PDF file
uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Reset session state for a new file
    if 'previous_uploaded_file' in st.session_state:
        if st.session_state.previous_uploaded_file != uploaded_file.name:
            st.session_state.page_ranges = []
            st.session_state.start_page = 1
    else:
        st.session_state.page_ranges = []
        st.session_state.start_page = 1
    st.session_state.previous_uploaded_file = uploaded_file.name

    # Read file data
    pdf_data = uploaded_file.read()
    document = fitz.open(stream=pdf_data, filetype="pdf")
    total_pages = len(document)

    # Input for custom page ranges
    st.markdown("<h4>أدخل نطاقات الصفحات لتقسيم الملف:</h4>", unsafe_allow_html=True)
    if 'page_ranges' not in st.session_state:
        st.session_state.page_ranges = []
        st.session_state.start_page = 1

    page_ranges = st.session_state.page_ranges
    start_page = st.session_state.start_page

    if start_page <= total_pages:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            start_page_input = st.number_input("من صفحة رقم", min_value=start_page, max_value=total_pages, step=1, key=f"start_input_{len(page_ranges)}")
        with col2:
            end_page = st.number_input("إلى صفحة رقم", min_value=start_page_input, max_value=total_pages, step=1, key=f"end_input_{len(page_ranges)}")
        with col3:
            doc_name = st.text_input("اسم المستند (اختياري)", value="", key=f"name_input_{len(page_ranges)}")
        if st.button('إضافة مستند'):
            page_ranges.append((start_page_input - 1, end_page - 1, doc_name))
            st.session_state.page_ranges = page_ranges
            st.session_state.start_page = end_page + 1

    # Display the added page ranges
    if page_ranges:
        st.markdown("### المستندات المضافة:")
        for idx, (start, end, name) in enumerate(page_ranges):
            st.write(f"{idx + 1}. من صفحة {start + 1} إلى صفحة {end + 1} - {name if name else 'بدون اسم'}")

    # Button to start splitting process
    if st.button('تحويل الآن'):
        try:
            # Create output folder in a temporary directory
            output_folder = "output_files"
            os.makedirs(output_folder, exist_ok=True)

            # Split PDF based on custom ranges
            output_files = split_pdf_custom_ranges(pdf_data, page_ranges, output_folder)

            # Create a ZIP file to compress the output files
            zip_filename = f"{uploaded_file.name.replace('.pdf', '')}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in output_files:
                    zipf.write(file, os.path.basename(file))

            # Provide download button for the ZIP file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="تحميل الكل كملف ZIP",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )

            st.success("تم تقسيم الملفات بنجاح وتحويلها إلى ملف مضغوط!")

        except ValueError:
            st.error("الرجاء التأكد من صحة التنسيق المدخل.")

        finally:
            # Clean up output files
            for file in output_files:
                if os.path.exists(file):
                    os.remove(file)
            if os.path.exists(zip_filename):
                os.remove(zip_filename)
