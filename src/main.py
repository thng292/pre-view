from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
import google.generativeai as genai
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from fastapi.middleware.cors import CORSMiddleware
import socketio

#load_dotenv('.env')
#genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = FastAPI()
sio=socketio.AsyncServer(async_mode="asgi", 
                         cors_allowed_origins="*",
                         max_http_buffer_size=10 * 1024 * 1024, # 10MB
                         transports=['websocket'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify a list of allowed origins, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = socketio.ASGIApp(sio)

app.mount("/socket.io/", socket_app)

# Socketio
async def response(sid, audio_data, text, enable_code):
    await sio.emit('response', {'audio': audio_data, 'text': text, 'enable_code': enable_code}, to=sid)

@sio.event
async def connect(sid, environ, auth=None):
    print("- New Client Connected to This id :"+" "+str(sid))

@sio.event
async def disconnect(sid):
    print("- Client Disconnected: "+" "+str(sid))

@sio.on('input_audio')
async def input_audio_process(sid, data):
    print("- Client: " + str(sid) + 'sent audio:')
    print('code: ' + data['code'])
    
    # testing
    with open('src\\test\\output_file.wav', 'wb') as file:
        file.write(data['audio'])
    with open('src\\test\\nu-luu-loat.wav', 'rb') as f:
        audio_data = f.read()
    await response(sid, audio_data, 'hello', True)

@sio.on('input_text')
async def input_audio_process(sid, data):
    print("- Client: " + str(sid) + 'sent text:')
    print('code: ' + data['code'])
    print('text: ' + data['text'])

    # testing
    with open('src\\test\\nu-luu-loat.wav', 'rb') as f:
        audio_data = f.read()
    await response(sid, audio_data, 'hello', True)

# Hosting web
templates = Jinja2Templates(directory="pre-view-frontend/dist")

app.mount('/assets', StaticFiles(directory="pre-view-frontend/dist/assets"), 'static')
#app.mount('/unity', StaticFiles(directory="pre-view-frontend/unity"), 'static')

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
