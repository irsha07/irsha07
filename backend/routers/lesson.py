# routers/lesson.py
from fastapi import APIRouter, HTTPException, Body
from services.lesson_planner import create_lesson_plan_step
from pydantic import BaseModel

router = APIRouter()

class LessonRequest(BaseModel):
    subject: str
    grade: str
    topic: str
    step: int
    previous_chunks: str = ""

@router.post("/lesson", tags=["Lesson Planning"])
async def get_lesson_content(request: LessonRequest):
    """
    Generates a single, stateful lesson step.
    Accepts the context from the previous step to generate the next one.
    """
    try:
        lesson_block, source_chunks = create_lesson_plan_step(
            request.subject,
            request.grade,
            request.topic,
            request.previous_chunks
        )
        
        return {
            "step": request.step, 
            "block": lesson_block,
            "source_chunks": source_chunks # Send the source text back to the frontend
        }
        
    except Exception as e:
        print(f"Error in lesson endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
