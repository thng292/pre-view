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
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from fastapi.middleware.cors import CORSMiddleware
import socketio

from xtts import Text2SpeechModule

dotenv.load_dotenv(".env")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    # system_instruction=""
)
chat_sessions = {}

tts = Text2SpeechModule()
tts.setSpeaker("model\\samples\\nu-luu-loat.wav")

app = FastAPI()
sio = socketio.AsyncServer(
    async_mode="asgi",
    connection_timeout=1000,
    ping_interval=100,
    ping_timeout=1000,
    cors_allowed_origins="*",
    max_http_buffer_size=100 * 1024 * 1024,  # 100MB
    transports=["websocket"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # or specify a list of allowed origins, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socketio
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io/", socket_app)


async def response(sid, audio_data, text, enable_code):
    await sio.emit(
        "response",
        {"audio": audio_data, "text": text, "enable_code": enable_code},
        to=sid,
    )


@sio.event
async def connect(sid, environ, auth=None):
    print("- New Client Connected to This id: " + str(sid))
    chat_sessions[str(sid)] = model.start_chat()


@sio.event
async def disconnect(sid):
    print("- Client Disconnected: " + str(sid))
    if str(sid) in chat_sessions:
        del chat_sessions[str(sid)]


async def processAudio(sid, data):
    if str(sid) in chat_sessions:
        if data["code"] != "":
            rep = chat_sessions[str(sid)].send_message(
                [{"mime_type": "audio/wav", "data": data["audio"]}, data["code"]]
            )
        else:
            rep = chat_sessions[str(sid)].send_message(
                {"mime_type": "audio/wav", "data": data["audio"]}
            )
        print("TTS running for text: " + rep.text)
        tts.predict(rep.text, "vi", f"temp\\{str(sid)}.wav")
        print("TTS finish")
        print("sending data")

        with open(f"temp\\{str(sid)}.wav", "rb") as f:
            audio_data = f.read()
        await response(sid, audio_data, rep.text, False)


async def processText(sid, data):
    if str(sid) in chat_sessions:
        if data["code"] != "":
            rep = chat_sessions[str(sid)].send_message(data["text"])
        else:
            rep = chat_sessions[str(sid)].send_message([data["text"], data["code"]])
        print("TTS running for text: " + rep.text)
        tts.predict(rep.text, "vi", f"temp\\{str(sid)}.wav")
        print("TTS finish")

        with open(f"temp\\{str(sid)}.wav", "rb") as f:
            audio_data = f.read()
        print("sending data")
        await response(sid, audio_data, rep.text, False)


@sio.on("input_audio")
async def input_audio_process(sid, data):
    print("- Client: " + str(sid) + "sent audio:")
    # testing
    print("code: " + data["code"])
    # with open('src\\test\\output_file.wav', 'wb') as file:
    #    file.write(data['audio'])
    sio.start_background_task(processAudio, sid, data)


@sio.on("input_text")
async def input_audio_process(sid, data):
    print("- Client: " + str(sid) + "sent text:")
    # testing
    print("code: " + data["code"])
    print("text: " + data["text"])
    sio.start_background_task(processText, sid, data)


# Hosting web
templates = Jinja2Templates(directory="pre-view-frontend/dist")

app.mount("/assets", StaticFiles(directory="pre-view-frontend/dist/assets"), "static")
# app.mount('/unity', StaticFiles(directory="pre-view-frontend/unity"), 'static')


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
