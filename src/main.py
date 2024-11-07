from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import os
import logging
import json
import dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="./Data/templates")

# Define a Pydantic model to structure the expected response
class JobExtractedInfo(BaseModel):
    companyName: str
    jobTitle: str
    jobLevel: str
    yoe: int
    programmingLanguages: list
    frameworks: list
    skills: list
    responsibilities: list

# Render the form for user input
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the endpoint for submitting the job description
@app.post("/extract-job-info", response_class=HTMLResponse)
async def extract_job_info(request: Request, job_description: str = Form(...)):
    # Define the prompt template
    prompt = f"""This is a job description of a job related to IT field: 
    \n\n{job_description}\n\nExtract the following information from the above paragraph and export it to valid JSON:
    Company name
    Job title
    Job level (intern, fresher, junior, senior)
    Year of experience (yoe)
    Programming languages
    Frameworks
    Skills
    Responsibilities

    Example:
    {{
        "companyName": "Google",
        "jobTitle": "Software developer",
        "jobLevel": "junior",
        "yoe": 1,
        "programmingLanguages": ["HTML", "CSS", "JavaScript"],
        "frameworks": ["ReactJS"],
        "skills": [
            "Object Oriented Programming",
            "Design Patterns",
            "Windows/Linux/MacOS development"
        ],
        "responsibilities": [
            "Analyze, design, develop and test software product features",
            "Produce technical solutions and implement them"
        ]
    }}

    Do not use markdown.
    Do not add more words to the JSON output; if you want to add a little thought or notes, use a comment instead."""

    # Load API key from environment variable
    dotenv.load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")
    
    # Send the prompt to the Google Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        api_response = response.json()
        logger.info("API Response: %s", api_response)  # Log the API response
        
        # Extract the job information from the response
        job_info = api_response['candidates'][0]['content']['parts'][0]['text']
        
        try:
            extracted_info = JobExtractedInfo(**json.loads(job_info))
            return templates.TemplateResponse("result.html", {"request": request, "info": extracted_info})
        except Exception as e:
            logger.error("Failed to parse JSON: %s", str(e))
            raise HTTPException(status_code=500, detail=f"Failed to parse JSON: {str(e)}")
    else:
        logger.error("Error with external API request: %s - %s", response.status_code, response.text)
        raise HTTPException(status_code=response.status_code, detail="Error with external API request: " + response.text)