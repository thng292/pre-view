import os, dotenv, logging, json, time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable
dotenv.load_dotenv(".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_flash = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = FastAPI()

templates = Jinja2Templates(directory="pre-view-frontend/dist")

app.mount("/assets", StaticFiles(directory="pre-view-frontend/dist/assets"), "static")
# app.mount('/unity', StaticFiles(directory="pre-view-frontend/unity"), 'static')


# Define a Pydantic model to structure the expected response
class JobExtractInput(BaseModel):
    jd: str


class JobExtractedOutput(BaseModel):
    companyName: Any
    jobTitle: Any
    jobLevel: Any
    yoe: Any
    programmingLanguages: list[Any]
    frameworks: list[Any]
    skills: list[Any]
    responsibilities: list[Any]


# Define the endpoint for submitting the job description
@app.post("/extract-job-info/", response_model=JobExtractedOutput)
async def extract_job_info(request: JobExtractInput):
    job_description = request.jd

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

    # Send the prompt to the Google Gemini API
    retry = 3
    for i in range(retry):
        try:
            logger.info("Sending request to gemini")
            before = time.time()
            response = gemini_flash.generate_content(
                prompt, generation_config={"temperature": i * 0.1}
            )
            logger.info("Gemini time taken %f", time.time() - before)
            return JobExtractedOutput(**json.loads(response.text))
        except Exception as e:
            logger.error("Failed to parse JSON: %s", str(e))

    raise HTTPException(status_code=400, detail=f"Couldn't process this")
