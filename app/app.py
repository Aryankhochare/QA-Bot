import streamlit as st
import uuid
from datetime import datetime
from qa_bot import *

# Set page config and remove default menu items
st.set_page_config(
    page_title="ChatBot",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        height: 600px;
        overflow-y: auto;
    }
    
    /* Message styling */
    .user-message {
        background-color: #e1e1e1;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: right;
    }
    
    .bot-message {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Better button styling */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        margin: 5px 0;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
    }
    
    /* Header styling */
    .main-header {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session states
if 'sessions' not in st.session_state:
    st.session_state.sessions = {}
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

def create_new_session():
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.sessions[session_id] = {
        'name': f"Chat {timestamp}",
        'files': [],
        'vector_store': None,
        'qa_chain': None
    }
    return session_id

# Sidebar
with st.sidebar:
    st.title("💬 Chat Sessions")
    st.divider()
    
    # New chat button with better styling
    if st.button("➕ New Chat", type="primary", use_container_width=True):
        session_id = create_new_session()
        st.session_state.current_session = session_id
        st.rerun()
    
    st.divider()
    
    # Session list with better organization
    for session_id, session in st.session_state.sessions.items():
        col1, col2 = st.columns([5,1])
        with col1:
            if st.button(
                f"📄 {session['name']}", 
                key=f"session_{session_id}",
                use_container_width=True,
                type="secondary" if session_id != st.session_state.current_session else "primary"
            ):
                st.session_state.current_session = session_id
                st.rerun()
        with col2:
            if st.button("🗑", key=f"delete_{session_id}"):
                if session_id in st.session_state.sessions:
                    del st.session_state.sessions[session_id]
                    if session_id in st.session_state.chat_history:
                        del st.session_state.chat_history[session_id]
                    if st.session_state.current_session == session_id:
                        st.session_state.current_session = None
                    st.rerun()

# Main content
if st.session_state.current_session is None:
    st.session_state.current_session = create_new_session()

current_session = st.session_state.sessions[st.session_state.current_session]

# Main header
st.markdown(f"<div class='main-header'><h2>💬 {current_session['name']}</h2></div>", unsafe_allow_html=True)

# File upload section
with st.expander("📁 Upload Documents", expanded=not current_session.get('files')):
    uploaded_files = st.file_uploader(
        "Drop your PDF files here",
        type="pdf",
        accept_multiple_files=True,
        key=f"upload_{st.session_state.current_session}"
    )
    
    if uploaded_files:
        if not current_session.get('qa_chain'):
            col1, col2, col3 = st.columns([3,2,3])
            with col2:
                if st.button("Process Documents", type="primary", use_container_width=True):
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    
                    # Process files
                    all_texts = []
                    for i, file in enumerate(uploaded_files):
                        progress = (i + 1) / len(uploaded_files)
                        progress_text.text(f"Processing {file.name}...")
                        progress_bar.progress(progress)
                        
                        text = extract_text_from_pdf(file)
                        all_texts.append(text)
                    
                    progress_text.text("Creating vector store...")
                    combined_text = "\n\n".join(all_texts)
                    chunks = chunk_text(combined_text)
                    vector_store = create_vector_store(chunks)
                    qa_chain = setup_qa_chain(vector_store)
                    
                    current_session['vector_store'] = vector_store
                    current_session['qa_chain'] = qa_chain
                    current_session['files'] = [f.name for f in uploaded_files]
                    
                    progress_bar.empty()
                    progress_text.empty()
                    st.success("Documents processed successfully!")
                    st.rerun()

# Display processed files
if current_session.get('files'):
    st.markdown("**📚 Processed Documents:**")
    for file in current_session['files']:
        st.markdown(f"- {file}")

# Chat interface
st.divider()

# Initialize chat history
if st.session_state.current_session not in st.session_state.chat_history:
    st.session_state.chat_history[st.session_state.current_session] = []

# Chat container
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.chat_history[st.session_state.current_session]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Input
if prompt := st.chat_input("Type your question here..."):
    if not current_session.get('qa_chain'):
        st.error("Please upload and process documents first!")
    else:
        # Add user message
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.chat_history[st.session_state.current_session].append(
            {"role": "user", "content": prompt}
        )
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_answer(current_session['qa_chain'], prompt)
                st.write(response)
        
        st.session_state.chat_history[st.session_state.current_session].append(
            {"role": "assistant", "content": response}
        )

# Rename session option
with st.sidebar:
    st.divider()
    if st.button("✏️ Rename Current Session", use_container_width=True):
        new_name = st.text_input(
            "Enter new name:",
            value=current_session['name'],
            key="rename_input"
        )
        if st.button("Save", type="primary"):
            current_session['name'] = new_name
            st.rerun()