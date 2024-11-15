import os, dotenv, logging, json, time
from fastapi import FastAPI, HTTPException
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


class JobExtractInput(BaseModel):
    jd: str


from extract_jd import JobExtractedOutput, extractJD


@app.post("/extract-job-info/", response_model=JobExtractedOutput)
async def extract_job_info(request: JobExtractInput):
    job_description = request.jd

    output = extractJD(job_description)
    if output:
        return output
    raise HTTPException(status_code=400, detail=f"Couldn't process this")
