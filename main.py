from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import uuid
import shutil
import tempfile
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional
import json

# Import document processing modules
from document_processor import extract_text_from_file
from ai_processor import process_with_llm

app = FastAPI(title="Intelligent Document Processing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create temp directory if it doesn't exist
os.makedirs("temp", exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file, extract text, and process with LLM
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1].lower().replace(".", "")
    
    # Check if file type is supported
    supported_extensions = ["pdf", "docx", "jpg", "jpeg", "png", "txt"]
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Supported types: {', '.join(supported_extensions)}"
        )
    
    # Create a temporary file
    temp_file_path = f"temp/{uuid.uuid4()}.{file_extension}"
    
    try:
        # Save uploaded file to temp location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from file
        raw_text = extract_text_from_file(temp_file_path, file_extension)
        
        if not raw_text:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to extract text from file"}
            )
        
        # Process with LLM to get structured data
        structured_data = process_with_llm(raw_text)
        
        # Return the results
        return {
            "structured_data": structured_data
        }
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/")
async def read_root():
    """
    Serve the main HTML page
    """
    try:
        print("Serving HTML page")
        # Fix: Add encoding="utf-8" to handle special characters
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
           
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>HTML file not found</h1>", status_code=404)
    except Exception as e:
        print(f"Error serving HTML: {str(e)}")
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8097, reload=True)