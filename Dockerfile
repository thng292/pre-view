# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM nikolaik/python-nodejs:python3.10-nodejs18

#FROM python:3.12

WORKDIR /app

COPY . /app 
#RUN apt-get update
#RUN apt-get -y install nodejs
#RUN apt-get -y install npm

WORKDIR /app/pre-view-frontend
RUN npm install
RUN npm run build
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "src/main.py"]
