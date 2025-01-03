import os
from huggingface_hub import snapshot_download


def downloadModel(force=False):
    model_path = "model/"
    model_id = "pre-view/viXTTS-ft-code"

    if os.path.exists(model_path) and not force:
        return
    os.makedirs(model_path, exist_ok=True)
    snapshot_download(
        repo_id=model_id,
        repo_type="model",
        local_dir=model_path,
    )
