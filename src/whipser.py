import time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

model_id = "openai/whisper-large-v3-turbo"

class Speech2TextModule:
    def __init__(self, device: str = "cuda:0", torch_dtype: torch.dtype = torch.float32):
        self.device = device
        self.torch_dtype = torch_dtype
        processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype)
        self.model.to(device)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            return_timestamps=True
        )
    
    def getText(self, path: str):
        res = self.pipe(path, generate_kwargs={"language": "vi", "num_beams": 1})
        return res["text"]

'''
stt = Speech2TextModule()
for i in range(0, 10):
    t = time.time()
    print(stt.getText('model/vi_sample.wav'))
    print(time.time() - t)
    time.sleep(5)
'''