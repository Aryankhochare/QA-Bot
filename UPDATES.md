### Update 01
- Created a new python project for QA Bot
- Installed required libraries: `pip install -r requirements.txt`
- Started with pdf procesing and text extraction using `PyPDF2` library

### Update 02
- Implemented text chunking to split text into sentences and then into words
- Used opeanai vector space model to calculate similarity between sentences and words
- Used quadrant using docker to store vector embiddings 

### Update 03
- started implementing the chatbot logic using the extracted text and vector embeddings
- Started testing the model using sample pdf data
- Implemented a simple user interface 
- Issues Faced
  - Vector embeddings were not being updated correctly
  - opeanai provides limited credits and due to big sample data , it was exceeding the limit
- Issues Resolved by
  - Implementing a workaround by using a smaller sample data and manually updating the vector embeddings
  - using new llm model , lama model

### Update 04
- Added HuggingFaceEmbeddings for embedding generation.
- Downloaded the GGUF model file: llama-2-7b-chat.gguf.
- Implemented llama_model.py to load the Llama model using llama_cpp.
- Resolved compatibility issues by creating LlamaLangChainWrapper to make llama_cpp LLM compatible with LangChain.
- Updated imports for HuggingFaceEmbeddings and Qdrant.
- Installed langchain-community and langchain-huggingface packages.
- Created a git repositary for the project and pushed all the code changes.

### Update 05
- Issues Faced
  - Large memory usage due to the size of the Llama model
  - Model was not able to process large pdf files due to memory constraints
  - Model was not able to handle multiple pdf files at once
  - Relatively slow processing speed due to the size of the Llama model
  - Due to Size of the model , it was giving issues to push the model to git 
- Issues Resolved by
- The memory issues was still there so tried uploding small pdfs and then tried to process them one by one
- The model was giving proper results but still processing was slow and also the git file will be heavy
- So tried to use a different llm model, Google Gemini model

### Update 06
- Stared implementing the Google Gemini model
- Installed necessary dependencies
- Used the google-generativeai library to interact with the API
- Set up environment variables for the Gemini API key (GENIUS_API_KEY)
- Combined document retrieval with the Gemini API
- Passed the prompt to the Gemini API to generate responses
- Built a user-friendly interface using Streamlit
- Built a user-friendly interface using Streamlit
- Integrated the RAG pipeline with the Streamlit
- Conducted end-to-end testing
  - Uploaded PDFs, processed them, and queried the chatbot
  - Verified response accuracy and interface usability.

### Update 07
- After all test were done, the model was giving proper results and the interface was user friendly
- The model was able to process large pdf files and was able to handle multiple pdf files at once
- The model was able to give proper results even when pdf files were large in size
- Commited all the updates on git and pushed the code to the repository
- Started doing minor changes and updates to the code to make it more efficient and user friendly

### Update 08
- Tried deploying the model on Streamlit
- Deployed the model on Streamlit
- Issues Faced
  1. Security and Cookie Issues:
    - Third-party cookie warnings in Chrome
    - Content Security Policy violations
    - Blocked resource loading
  2. Streamlit Platform Limitations:
    - Limited control over iframe behavior
    - Streamlit-specific CSS and styling constraints
    - Restricted access to certain browser features
  3. Performance Concerns:
    - Script loading delays
    - Resource blocking affecting load times  