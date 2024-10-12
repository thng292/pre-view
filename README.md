---
title: Pre:view
sdk: docker
app_port: 8000
---

### Setup Env

```
python -m venv .venv

source .venv/bin/activate (Linux)
venv\Scripts\Activate.ps1 (Windows Powershell)

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run app

```
fastapi dev src/main.py
```
