# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM nikolaik/python-nodejs:python3.10-nodejs18

# Set the working directory to the user's home directory
WORKDIR /app
COPY . /app 

WORKDIR /app/pre-view-frontend
RUN npm ci
RUN npm run build

WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod 777 /app
CMD ["fastapi", "run", "src/main.py"]
