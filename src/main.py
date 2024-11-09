from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv('.env')

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!"}
