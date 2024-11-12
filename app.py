import PyPDF2
import streamlit as st

# دالة لفصل ملف PDF باستخدام PyPDF2
def split_pdf(pdf):
    reader = PyPDF2.PdfReader(pdf)
    documents = []
    output_files = []

    current_document = PyPDF2.PdfWriter()
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text = page.extract_text()

        # التحقق من كون الصفحة بيضاء بناءً على النص
        if text is None or text.strip() == "":
            if current_document.get_num_pages() > 0:
                documents.append(current_document)
                current_document = PyPDF2.PdfWriter()
            continue

        current_document.add_page(page)

    if current_document.get_num_pages() > 0:
        documents.append(current_document)

    # حفظ الملفات المؤقتة
    for idx, doc in enumerate(documents):
        doc_name = f"document_{idx + 1}.pdf"
        with open(doc_name, "wb") as f:
            doc.write(f)
        output_files.append(doc_name)

    return output_files

# إنشاء واجهة Streamlit
st.title("PDF Splitter by Blank Page")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.write("Processing...")
    output_files = split_pdf(uploaded_file)

    for output_file in output_files:
        with open(output_file, "rb") as f:
            st.download_button(
                label=f"Download {output_file}",
                data=f,
                file_name=output_file,
                mime="application/pdf"
            )

    st.success("PDF splitting completed successfully!")
