FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

RUN apt install wget
RUN wget -O /app/table_detection/model_files/ICDAR.19.Track.B2.Modern.table.structure.recognition.v2.pth --no-check-certificate 'https://drive.google.com/u/1/uc?id=1-QieHkR1Q7CXuBu4fp3rYrvDG9j26eFT&export=download'


RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install mmdet==2.3.0 requests && \
pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
pip install mmcv-full==1.0.5 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.5.0/index.html	

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
