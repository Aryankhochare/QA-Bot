import streamlit as st
from qa_bot import *

st.title("Document QA Bot")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Process PDF
    text = extract_text_from_pdf(uploaded_file)
    chunks = chunk_text(text)
    vector_store = create_vector_store(chunks)
    qa_chain = setup_qa_chain(vector_store)
    
    # Question input
    question = st.text_input("Ask a question about your document:")
    if question:
        answer = get_answer(qa_chain, question)
        st.write("Answer:", answer)