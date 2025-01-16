from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Chunk text into smaller parts."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# Test function
if __name__ == "__main__":
    pdf_path = "C:/Users/DELL/Desktop/QA-BOT/data/sample.pdf"  # Replace with the path to your PDF
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    print(f"Generated {len(chunks)} chunks.")
    print(chunks[:5])  # Print the first 5 chunks
