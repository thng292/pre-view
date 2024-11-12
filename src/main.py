from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
import google.generativeai as genai
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

'''
load_dotenv('.env')
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
'''

app = FastAPI()

templates = Jinja2Templates(directory="pre-view-frontend/dist")

app.mount('/assets', StaticFiles(directory="pre-view-frontend/dist/assets"), 'static')
#app.mount('/unity', StaticFiles(directory="pre-view-frontend/unity"), 'static')

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
