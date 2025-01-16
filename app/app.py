import streamlit as st
from qa_bot import *

st.title("Document QA Bot")

# Multiple file upload
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # Initialize progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process all PDFs
    all_texts = []
    for i, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Extract text from each PDF
        text = extract_text_from_pdf(uploaded_file)
        all_texts.append(text)
    
    # Combine all texts
    combined_text = "\n\n".join(all_texts)
    
    # Process combined text
    status_text.text("Chunking text...")
    chunks = chunk_text(combined_text)
    
    status_text.text("Creating vector store...")
    vector_store = create_vector_store(chunks)
    
    status_text.text("Setting up QA chain...")
    qa_chain = setup_qa_chain(vector_store)
    
    # Clear status messages
    status_text.empty()
    progress_bar.empty()
    
    # Show success message
    st.success(f"Successfully processed {len(uploaded_files)} files!")
    
    # Display file names
    st.write("Processed files:")
    for file in uploaded_files:
        st.write(f"- {file.name}")
    
    # Question input
    question = st.text_input("Ask a question about your documents:")
    if question:
        with st.spinner("Generating answer..."):
            answer = get_answer(qa_chain, question)
            st.write("Answer:", answer)

    # Add a clear button to reset the session
    if st.button("Clear All"):
        st.session_state.clear()
        st.experimental_rerun()