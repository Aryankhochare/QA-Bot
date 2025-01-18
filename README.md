### 📖 Project Overview
The Simple Q&A Chatbot with RAG and LangChain is designed to understand and answer questions based on the content of PDF documents, such as course materials or company documentation. By leveraging Retrieval-Augmented Generation (RAG), the system retrieves relevant document content and uses a Large Language Model (LLM) to provide contextually accurate answers.
This project integrates cutting-edge tools like LangChain for document processing and embeddings, Qdrant for vector storage, and a web interface for user interactions.

### Setup To run Project on your machine
1. Clone the Repository
2. Set Up a Virtual Environment
   - Create virtual environment (python -m venv venv)
   - Activate the virtual environment (venv\Scripts\activate)
3. Install Dependencies(pip install -r requirements.txt)
4. Create a .env file in root directory and paste your goolge api key
5. Run the project (streamlit run app/app.py)

### 🎯 Goals
Build a Working Prototype

- Process PDF documents and convert them into text chunks.
- Use RAG architecture to retrieve and answer questions based on document content.
- Provide relevant responses via a web-based chat interface.
- Document processing using LangChain.
- Generate and manage vector embeddings for document content.
- Implement a retrieval-based QA system using RAG architecture.
- Integrate a Large Language Model (LLM) for contextual responses.

### 🛠️ Technical Stack
- Programming Language: Python 3.9+
- Document Processing: LangChain
- Vector Storage: Qdrant
- Large Language Model: Google Gemini AI
- Web Interface: Streamlit
