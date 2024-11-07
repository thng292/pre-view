import os
from huggingface_hub import snapshot_download

model_path = "model/"
model_id = "capleaf/viXTTS"

os.makedirs(model_path, exist_ok=True)
snapshot_download(
    repo_id=model_id,
    repo_type="model",
    local_dir=model_path,
)