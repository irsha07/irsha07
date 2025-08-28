# services/pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os

CHROMA_DB_PATH = "data/chroma"

def load_and_process_pdf(file_path: str, filename: str, grade: str):
    """
    Loads a PDF, splits it into chunks, and ingests it into a Chroma vector store.
    The collection name is now a combination of the grade and the filename.
    """
    print(f"Processing '{filename}' for grade {grade}...")
    
    # 1. Load the document
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # 3. Create a unique, structured collection name
    base_name = os.path.splitext(filename)[0].lower().replace("-", "_").replace(" ", "_")
    collection_name = f"grade_{grade}_{base_name}"
    
    # 4. Create embeddings and ingest into ChromaDB
    embeddings = OpenAIEmbeddings()
    Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_name=collection_name
    )
    
    print(f"Successfully processed and saved to collection '{collection_name}'.")
