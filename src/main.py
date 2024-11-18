import os, dotenv, logging, socketio

dotenv.load_dotenv(".env")
import google.generativeai as genai
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from .xtts import Text2SpeechModule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
)
chat_sessions = {}

tts = Text2SpeechModule()
tts.setSpeaker("model/samples/nu-luu-loat.wav")

app = FastAPI()
sio = socketio.AsyncServer(
    async_mode="asgi",
    connection_timeout=1000,
    ping_interval=100,
    ping_timeout=1000,
    cors_allowed_origins=["*", "http://localhost:5173"],  # Replace with your frontend origin
    max_http_buffer_size=100 * 1024 * 1024,  # 100MB
    transports=["websocket", "polling"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://hoppscotch.io",  # Testing
        "http://localhost:5173"
        "*",  # Testing
    ],  # or specify a list of allowed origins, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socketio
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)


async def response(sid, audio_data, text, enable_code):
    await sio.emit(
        "response",
        {"audio": audio_data, "text": text, "enable_code": enable_code},
        to=sid,
    )


@sio.event
async def connect(sid, environ, auth=None):
    logger.info("- New Client Connected to This id: " + str(sid))
    chat_sessions[str(sid)] = model.start_chat()


@sio.event
async def disconnect(sid):
    logger.info("- Client Disconnected: " + str(sid))
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
        logger.info("TTS running for text: " + rep.text)
        audio_data = tts.predict(rep.text, "en")
        logger.info("TTS finish")
        logger.info("sending data")

        await response(sid, audio_data, rep.text, False)


async def processText(sid, data):
    if str(object=sid) in chat_sessions:
        if data["code"] != "":
            rep = chat_sessions[str(sid)].send_message(data["text"])
        else:
            rep = chat_sessions[str(sid)].send_message([data["text"], data["code"]])
        logger.info("TTS running for text: " + rep.text)
        audio_data = tts.predict(rep.text, "en")
        logger.info("TTS finish")

        logger.info("sending data")
        await response(sid, audio_data, rep.text, False)


@sio.on("input_audio")
async def input_audio_process(sid, data):
    logger.info("- Client: " + str(sid) + "sent audio:")
    # testing
    logger.info("code: " + data["code"])
    sio.start_background_task(processAudio, sid, data)


@sio.on("input_text")
async def input_text_process(sid, data):
    logger.info("- Client: " + str(sid) + "sent text:")
    # testing
    logger.info("code: " + data["code"])
    logger.info("text: " + data["text"])
    sio.start_background_task(processText, sid, data)


# Hosting web
templates = Jinja2Templates(directory="pre-view-frontend/dist")

# app.mount("/assets", StaticFiles(directory="pre-view-frontend/dist/assets"), "static")
# app.mount('/unity', StaticFiles(directory="pre-view-frontend/unity"), 'static')


@app.get("/")
#async def root(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})
    # return HTMLResponse(open("src/test/test.html").read())


class JobExtractInput(BaseModel):
    jd: str


from .extract_jd import JobExtractedOutput, extractJD


@app.post("/api/jd/", response_model=JobExtractedOutput)
async def extract_job_info(request: JobExtractInput):
    job_description = request.jd

    output = extractJD(job_description)
    if output:
        return output
    raise HTTPException(status_code=400, detail=f"Couldn't process this")
