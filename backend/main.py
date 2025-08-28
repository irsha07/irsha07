# main.py
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import lesson, chat, upload, knowledge # Import the new router
import uvicorn

# Create necessary directories
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/chroma", exist_ok=True)

app = FastAPI(
    title="AI Teacher Backend",
    description="Backend to power the learnpal.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routers
app.include_router(lesson.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(knowledge.router) # Add the new router here

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the AI Teacher backend!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
