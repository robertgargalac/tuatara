FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt
