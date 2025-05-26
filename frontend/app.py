import streamlit as st
import pdfplumber
import sys
import os

st.set_page_config(
    page_title="Askify – Ask from any paragraph or PDF",
    page_icon="🧠",  # Or use a custom icon file
    layout="centered"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rag_logic import retrieve_top_k_contexts, build_prompt, generate_answer

st.title("Askify – Ask from any paragraph or PDF")
st.markdown(
    """
    💬 **Askify** lets you upload a PDF or paste any paragraph and ask questions about it.  
    Powered by retrieval and generative model, it gives context-aware answers in seconds.

    🔍 [Click here to view the system architecture](https://drive.google.com/file/d/1K1R3iNRlxGrG0Krg2ELud9ZiJeZoqkWx/view?usp=sharing)
    """,
    unsafe_allow_html=True
)



input_mode = st.radio("Choose input type:", ["Type or Paste Text", "Upload PDF"])

context = ""

if input_mode == "Type or Paste Text":
    context = st.text_area("Enter your paragraph:", height=250)

elif input_mode == "Upload PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf_file:
        try:
            with pdfplumber.open(pdf_file) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += page_text + "\n"
            context = pdf_text
            st.text_area("Extracted PDF Text (editable):", value=pdf_text, height=250, key="pdf_text")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- Question Input ---
question = st.text_input("Ask a question based on the context:")

# --- Submit Button ---
if st.button("Submit"):
    with st.spinner("Thinking..."):
        if context and question:
            try:
                contexts = retrieve_top_k_contexts(question, context)
                prompt = build_prompt(question, contexts)
                answer = generate_answer(prompt)

                st.success("Answer:")
                st.write(answer)
                st.write("Context Used to answer your question:")
                st.write(contexts[0])  # first relevant chunk
            except Exception as e:
                st.error(f"Error during processing: {e}")
        else:
            st.error("Please provide both context and a question.")

# streamlit run frontend/app.py