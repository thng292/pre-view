---
title: Pre:view
sdk: docker
app_port: 8000
---
### Setup Env

Run following command

```
python -m venv .venv

source .venv/bin/activate (Linux)
.venv\Scripts\Activate.ps1 (Windows Powershell)

python -m pip install --upgrade pip
pip install -r requirements.txt

python src/download_model.py
```

Change following line in `.venv\Lib\site-packages\TTS\tts\layers\xtts\tokenizer.py`

line 614 add: 

```
"vi": 250,
```

line 643 add: 

```
elif lang =="vi":

    txt = basic_cleaners(txt)
```

Change following line in `.venv\Lib\site-packages\TTS\tts\configs\xtts_config.py`

line 92 add:

```
"vi"
```

### Run app

```
fastapi dev src/main.py
```
