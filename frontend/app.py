import streamlit as st
import requests

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag_logic import retrieve_top_k_contexts, build_prompt, generate_answer

st.title("Ask Questions Based on Your Paragraph")

context = st.text_area("Enter your paragraph:",height=250)
question = st.text_input("Ask a question based on the paragraph:")


if st.button("Submit"):
    with st.spinner("Thinking..."):
        if context and question:
            contexts = retrieve_top_k_contexts(question)
            prompt = build_prompt(question, contexts)
            answer = generate_answer(prompt)

            st.success("Answer:")
            st.write("Context Used to answer your question:")
            st.write(contexts[0])  # first chunk used
            st.write(answer)
        else:
            st.error("Please provide both context and a question.")

# streamlit run frontend/app.py