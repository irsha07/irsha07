# routers/upload.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.pdf_loader import load_and_process_pdf
import os

router = APIRouter()
UPLOAD_DIRECTORY = "data/uploads"

@router.post("/upload", tags=["Knowledge Base"])
async def upload_pdf(
    grade: str = Form(...), 
    file: UploadFile = File(...)
):
    """
    Uploads a PDF for a specific grade, saves it, and processes it into the knowledge base.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are accepted.")

    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        # Process the PDF into the vector store, now including the grade
        load_and_process_pdf(file_path, file.filename, grade)
        
        return {"message": f"Successfully uploaded '{file.filename}' for grade {grade}."}
    except Exception as e:
        print(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
