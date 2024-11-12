import fitz  # PyMuPDF
import os
import numpy as np
import streamlit as st

# دالة لفصل ملف PDF
def split_pdf(pdf):
    document = fitz.open(stream=pdf.read(), filetype="pdf")

    current_document = None
    documents = []
    output_files = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)

        # التحقق إذا كانت الصفحة بيضاء (الفاصل) بناءً على النص ومستوى النصوع
        text = page.get_text().strip()
        pix = page.get_pixmap()

        # تحويل صورة الصفحة إلى مصفوفة لتحليل مستوى النصوع
        image_data = np.frombuffer(pix.samples, dtype=np.uint8)

        # إذا كان متوسط النصوع عالياً بما يكفي، نعتبر الصفحة بيضاء
        average_luminance = image_data.mean()
        
        if len(text) == 0 and average_luminance > 245:
            # إغلاق الوثيقة الحالية إذا وجدت
            if current_document is not None:
                documents.append(current_document)
                current_document = None
            continue

        # إذا كانت هناك دعوى، البدء أو إضافة الصفحة إلى الوثيقة
        if current_document is None:
            current_document = fitz.open()  # إنشاء وثيقة جديدة
        current_document.insert_pdf(document, from_page=page_number, to_page=page_number)

    # إضافة الوثيقة الأخيرة إذا وجدت
    if current_document is not None:
        documents.append(current_document)

    # حفظ الملفات المؤقتة
    for idx, doc in enumerate(documents):
        doc_name = f"document_{idx + 1}.pdf"
        doc.save(doc_name)
        output_files.append(doc_name)
        doc.close()

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
