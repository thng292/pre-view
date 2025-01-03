import os

LOAD_TTS = "LOAD_TTS" in os.environ and os.environ["LOAD_TTS"] == "1"

from io import BytesIO
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from .download_model import downloadModel

model_path = "model/"


class TTSModule:
    def __init__(self):
        downloadModel()
        config = XttsConfig()
        config.load_json(model_path + "config.json")
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config, checkpoint_dir=model_path)
        self.model.eval()
        if torch.cuda.is_available():
            self.model.cuda()
        self.gpt_cond_latent = None
        self.speaker_embedding = None

    def setSpeaker(self, speaker_wav: str):
        self.gpt_cond_latent, self.speaker_embedding = (
            self.model.get_conditioning_latents(
                audio_path=speaker_wav, gpt_cond_len=30, gpt_cond_chunk_len=4
            )
        )

    def predict(self, prompt, language):
        if self.gpt_cond_latent == None or self.speaker_embedding == None:
            return
        out = self.model.inference(
            prompt,
            language,
            self.gpt_cond_latent,
            self.speaker_embedding,
            repetition_penalty=5.0,
            temperature=0.75,
            enable_text_splitting=True,
        )
        buffer = BytesIO()
        torchaudio.save(
            buffer, torch.tensor(out["wav"]).unsqueeze(0), 24000, format="wav"
        )
        buffer.seek(0)
        return buffer.read()


class NoTTS:
    def __init__(self):
        pass

    def setSpeaker(self, speaker_wav: str):
        pass

    def predict(self, prompt, language):
        return open("output.wav", "rb").read()


Text2SpeechModule = TTSModule if LOAD_TTS else NoTTS

"""
tts = Text2SpeechModule()
tts.setSpeaker('model/samples/nu-luu-loat.wav')

for i in range(10):
    t = time.time()
    tts.predict("Trường Đại học Khoa học Tự nhiên là trường đại học đầu ngành về đào tạo, nghiên cứu khoa học cơ bản, khoa học công nghệ và ứng dụng ở miền Nam Việt Nam.",
            'vi',f'output{i}.wav')
    print(time.time() - t)
    time.sleep(5)
"""
