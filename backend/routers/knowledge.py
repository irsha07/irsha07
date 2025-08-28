# routers/knowledge.py
from fastapi import APIRouter, HTTPException
import chromadb
import os

router = APIRouter()
CHROMA_DB_PATH = "data/chroma"

@router.get("/subjects", tags=["Subjects"])
async def get_subjects():
    """
    Returns a list of all available knowledge base collections (subjects).
    """
    if not os.path.exists(CHROMA_DB_PATH):
        return []
    try:
        # Use the modern way to connect to ChromaDB
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collections = client.list_collections()
        subject_names = [col.name for col in collections]
        return subject_names
    except Exception as e:
        print(f"Error listing collections: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve subjects from the knowledge base.")

