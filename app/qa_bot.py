# Import necessary libraries
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Chunk text into smaller parts."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def create_vector_store(text_chunks):
    """Create and return a vector store from text chunks."""
    # Initialize Google's embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    
    # Create vector store
    vector_store = Qdrant.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        location=":memory:"  # For development, store in memory
    )
    
    return vector_store

def setup_qa_chain(vector_store):
    """Set up the QA chain with Gemini."""
    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )
    
    # Create prompt template
    prompt_template = """
    Answer the question based on the context provided. If you don't know the answer, 
    just say you don't know. Don't try to make up an answer.
    
    Context: {context}
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return chain

def get_answer(chain, question):
    """Get answer for a question using the QA chain."""
    try:
        response = chain.run(question)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Main execution
if __name__ == "__main__":
    # Example usage
    pdf_path = "c:/Users/DELL/Desktop/QA-Bot/data/sample.pdf"
    
    # Process PDF
    raw_text = extract_text_from_pdf(pdf_path)
    text_chunks = chunk_text(raw_text)
    
    # Create vector store
    vector_store = create_vector_store(text_chunks)
    
    # Setup QA chain
    qa_chain = setup_qa_chain(vector_store)
    
    # Example question
    question = "What is this document about?"
    answer = get_answer(qa_chain, question)
    print(f"Q: {question}\nA: {answer}")