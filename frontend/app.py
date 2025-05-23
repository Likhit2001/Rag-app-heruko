import streamlit as st
import requests

st.title("Ask Questions Based on Your Paragraph")

context = st.text_area("Enter your paragraph:",height=250)
question = st.text_input("Ask a question based on the paragraph:")



if st.button("Submit"):
    with st.spinner("Thinking..."):

        response = requests.post(
            "http://localhost:8000/ask",
            json={"context": context , "question": question}
        )

        if response.status_code == 200:
            st.success("Answer:")
            st.write("Context Used to answer your question")
            st.write(response.json()["context"][0])
            st.write(response.json()["answer"])
        else:
            st.error("Something went wrong.")


# streamlit run frontend/app.py