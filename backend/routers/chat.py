# routers/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_engine import get_rag_response

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat", tags=["Chat"])
async def handle_chat(request: ChatRequest, subject: str, grade: str, topic: str):
    """
    Handles a user's freeform question using the RAG engine.
    """
    try:
        answer = get_rag_response(request.question, subject)
        # The frontend expects the answer in a specific format for chat
        return {"answer": answer}
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to get a response from the RAG engine.")
