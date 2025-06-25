import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
if os.getenv("OPENAI_API_KEY") is None:
    raise EnvironmentError("OPENAI_API_KEY not found in .env file.")
import json

from typing import Dict, Any, Optional, List  
import requests
from pydantic import BaseModel
from openai import OpenAI

# Get OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")


# Define Pydantic models for structured output
class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
   

class KeyDates(BaseModel):
    submission_deadline: Optional[str] = None
    pre_bid_meeting: Optional[str] = None
    contract_award: Optional[str] = None
    pre_bid_comments: Optional[str] = None

class RFPResponse(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    eligibility_criteria: Optional[List[str]] = None
    key_dates: Optional[KeyDates] = None
    key_points: Optional[List[str]] = None
    contact_info: Optional[ContactInfo] = None

def process_with_llm(text: str) -> Optional[Dict[str, Any]]:
    """
    Process extracted text with LLM to get structured data using OpenAI's structured output
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OpenAI API key not found in environment variables")
        return None
        
    try:
        # Initialize OpenAI client
        openai_client = OpenAI(api_key=api_key)
        
        # System prompt tailored for RFP analysis
        system_prompt = """You are a precise RFP analysis tool designed to analyze Request for Proposal (RFP) documents. Your task is to parse the provided RFP text and extract structured data.

        INSTRUCTIONS:
        - Analyze the provided RFP text carefully and extract key information.
        - For title: Extract the official RFP title or project name.
        - For summary: Provide a concise summary of the RFP's purpose and scope (max 100 words).
        - For eligibility_criteria: List all eligibility requirements for bidders (qualifications, certifications, experience requirements).
        - For key_dates: Extract important dates including:
          * submission_deadline: Final date for proposal submission
          * pre_bid_meeting: Date of pre-bid conference/meeting. If no pre-bid meeting date is mentioned, include any pre-bid meeting references or comments as "pre_bid_comments".
          * contract_award: Expected contract award date
          * pre_bid_comments: Any additional pre-bid related information
        - For key_points: list critical information like scope of work, deliverables, evaluation criteria, budget constraints with a little brief explanation of what it means and why it's important for the RFP.
        - For contact_info: Extract contact details including name, email, phone.
        - Use appropriate data types and not defined values for missing information.
        - Ensure all extracted information is accurate and relevant to the RFP context."""
        
        # Generate structured response using OpenAI API
        response = openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this RFP document and extract structured data: {text}"}
            ],
            temperature=0.6,
            max_completion_tokens=2046,
            response_format=RFPResponse
        )
        
        # Extract the parsed response
        rfp_data = response.choices[0].message.parsed
        
        # Convert Pydantic model to dictionary
        if rfp_data:
            return rfp_data.model_dump()
        else:
            print("Error: Failed to parse structured data from LLM response")
            return None
            
    except Exception as e:
        print(f"Error processing text with LLM: {str(e)}")
        return None