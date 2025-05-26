# import streamlit as st
# import requests

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from backend.rag_logic import retrieve_top_k_contexts, build_prompt, generate_answer

# st.title("Ask Questions Based on Your Paragraph")

# context = st.text_area("Enter your paragraph:",height=250)
# question = st.text_input("Ask a question based on the paragraph:")


# if st.button("Submit"):
#     with st.spinner("Thinking..."):
#         if context and question:
#             contexts = retrieve_top_k_contexts(question, context) 
#             prompt = build_prompt(question, contexts)
#             answer = generate_answer(prompt)

#             st.success("Answer:")
#             st.write("Context Used to answer your question:")
#             st.write(contexts[0])  # first chunk used
#             st.write(answer)
#         else:
#             st.error("Please provide both context and a question.")

import streamlit as st
import pdfplumber
import sys
import os

# Add backend logic path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rag_logic import retrieve_top_k_contexts, build_prompt, generate_answer

# --- Input Mode Selection ---
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
        if context.strip() and question.strip():
            try:
                contexts = retrieve_top_k_contexts(question, context)
                prompt = build_prompt(question, contexts)
                answer = generate_answer(prompt)

                st.success("Answer:")
                st.write("Context Used to answer your question:")
                if contexts:
                    st.write(contexts[0])  # first relevant chunk
                else:
                    st.warning("No relevant context was found.")
                st.write(answer)
            except Exception as e:
                st.error(f"Error during processing: {e}")
        else:
            st.error("Please provide both context and a question.")

# streamlit run frontend/app.py