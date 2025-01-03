import os, dotenv, logging, socketio
import google.generativeai as genai

dotenv.load_dotenv(".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from vinorm import TTSnorm
from enum import Enum
from .xtts import Text2SpeechModule
from .interviewAI import InterviewAI
from .stt import speech_to_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable

interview = None


class SupportedLanguage(str, Enum):
    vi = "vi"
    en = "en"


LANGUAGE_MAP: dict[SupportedLanguage, str] = {
    SupportedLanguage.vi: "Vietnamese",
    SupportedLanguage.en: "English",
}

LANGUAGE_MAP_R: dict[str, SupportedLanguage] = {
    "Vietnamese": SupportedLanguage.vi,
    "English": SupportedLanguage.en,
}

tts = Text2SpeechModule()
tts.setSpeaker("model/vi_sample.wav")

app = FastAPI()
sio = socketio.AsyncServer(
    async_mode="asgi",
    connection_timeout=1000,
    ping_interval=100,
    ping_timeout=1000,
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
    ],  # Replace with your frontend origin
    max_http_buffer_size=100 * 1024 * 1024,  # 100MB
    transports=["websocket"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://hoppscotch.io",  # Testing
        "http://localhost:5173",
    ],  # or specify a list of allowed origins, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socketio
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io/", socket_app)


async def response(sid, data):
    await sio.emit(
        "response",
        data,
        to=sid,
    )


@sio.event
async def connect(sid, environ, auth=None):
    logger.info("- New Client Connected to This id: " + str(sid))


@sio.event
async def disconnect(sid):
    logger.info("- Client Disconnected: " + str(sid))


def chat(userInp: str):
    if interview is None:
        return
    resp = interview.chat(userInp)
    normalized = TTSnorm(
        resp.text,
        unknown=False,
        lower=False,
        rule=True,
    )
    logger.info("Normalized: " + normalized)
    audio_data = tts.predict(normalized, LANGUAGE_MAP_R[interview.language])
    logger.info("TTS finish")

    return dict(audio=audio_data, enableCode=resp.switch_to_code, text=resp.text)


audioKey = "fromAudio"


async def processAudio(sid, data):
    logger.info("Converting STT")
    text = speech_to_text(data["audio"])
    logger.info("Converted: " + text)
    result = chat(text)
    if result is None:
        await response(sid, {})
        return
    result["userText"] = text
    await response(sid, result)


async def processText(sid, data):
    result = chat(data["text"])
    if result is None:
        await response(sid, {})
        return
    await response(sid, result)


@sio.on("input_audio")
async def input_audio_handler(sid, data):
    logger.info(msg="- Client: " + str(sid) + "sent audio")
    sio.start_background_task(processAudio, sid, data)


@sio.on("input_code")
async def input_code_handler(sid, data):
    logger.info("- Client: " + str(sid) + "sent code")
    sio.start_background_task(processText, sid, {"text": data["code"]})


@sio.on("input_text")
async def input_text_handler(sid, data):
    logger.info("- Client: " + str(sid) + "sent text")
    sio.start_background_task(processText, sid, data)


# Hosting web
templates = Jinja2Templates(directory="pre-view-frontend/dist")

app.mount("/assets", StaticFiles(directory="pre-view-frontend/dist/assets"), "static")
app.mount("/unity", StaticFiles(directory="pre-view-frontend/unity"), "static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class StartArgs(BaseModel):
    language: SupportedLanguage
    jd: str


@app.post("/api/start")
async def start(args: StartArgs):
    global interview
    interview = InterviewAI(
        language=LANGUAGE_MAP[args.language], job_description=args.jd
    )
    return (
        genai.GenerativeModel(
            system_instruction="You are a text formatter assistant. Your task is to take unstructured text and convert it into a well-organized Markdown document. The output should be clear, readable, and well-structured"
        )
        .generate_content(args.jd)
        .text
    )
    print(res)
    return res


# return HTMLResponse(open("src/test/test.html").read())
