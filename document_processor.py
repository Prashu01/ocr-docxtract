import os
import subprocess
import tempfile
from typing import Optional
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# PaddleOCR initialization (global instance to avoid reloading model)
from paddleocr import PaddleOCR
# Initialize PaddleOCR with English as default language
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_file(file_path: str, file_extension: str) -> Optional[str]:
    """
    Extract text from different file types
    """
    try:
        if file_extension == "pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return extract_text_from_docx(file_path)
        elif file_extension in ["jpg", "jpeg", "png"]:
            return extract_text_from_image(file_path)
        elif file_extension == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        print(f"Error extracting text from {file_extension} file: {str(e)}")
        return None

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF files using PyPDF2
    """
    try:
        import PyPDF2
        
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        # If PyPDF2 fails to extract text (e.g., scanned PDF), try OCR
        if not text.strip():
            return extract_text_from_pdf_with_ocr(file_path)
            
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        # Fallback to OCR
        return extract_text_from_pdf_with_ocr(file_path)

def extract_text_from_pdf_with_ocr(file_path: str) -> str:
    """
    Extract text from scanned PDF files using PaddleOCR
    """
    try:
        import pdf2image
        
        # Convert PDF to images
        images = pdf2image.convert_from_path(file_path)
        
        # Extract text from each image using PaddleOCR
        text = ""
        for i, image in enumerate(images):
            # Save the image temporarily
            temp_img_path = f"temp_page_{i}.jpg"
            image.save(temp_img_path)
            
            # Process with PaddleOCR
            result = ocr.ocr(temp_img_path, cls=True)
            
            # Extract text from OCR results
            page_text = ""
            for line in result[0]:
                if line:  # Check if line is not empty
                    # line[1][0] contains the actual text
                    page_text += line[1][0] + " "
            
            text += page_text + "\n"
            
            # Remove temp image
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
        return text
    except Exception as e:
        print(f"Error extracting text from PDF with OCR: {str(e)}")
        return "Failed to extract text from scanned PDF. Make sure PaddleOCR is properly installed."

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX files using python-docx
    """
    try:
        import docx
        
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from images using PaddleOCR
    """
    try:
        # Process with PaddleOCR
        result = ocr.ocr(file_path, cls=True)
        
        # Extract text from OCR results
        text = ""
        for line in result[0]:
            if line:  # Check if line is not empty
                # line[1][0] contains the actual text
                text += line[1][0] + " "
        
        return text
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return "Failed to extract text from image. Make sure PaddleOCR is properly installed and configured."