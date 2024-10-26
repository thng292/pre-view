import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import json

'''
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
'''

#device = "cpu"
#torch_dtype =  torch.float32

device = "cuda:0"
torch_dtype =  torch.float16

#model_id = "vinai/PhoWhisper-small"
model_id = "openai/whisper-large-v3-turbo"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
model.to(device)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
    return_timestamps=True
)

result = pipe("whisper/clip_388157_448157.mp3")
#print(result["text"])
#print(result['chunks'])
with open('whisper/sub.json', 'w') as file:
    json.dump(result['chunks'], file, indent=4,ensure_ascii=False)