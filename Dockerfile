# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM nikolaik/python-nodejs:python3.10-nodejs18

# https://huggingface.co/docs/hub/spaces-sdks-docker#permissions
# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app
COPY --chown=user . $HOME/app 


WORKDIR $HOME/app/pre-view-frontend
RUN npm ci
RUN npm run build


WORKDIR $HOME/app
RUN python -m pip install --upgrade pip
COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["fastapi", "run", "src/main.py"]
