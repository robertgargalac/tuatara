import multiprocessing
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from utils import b64_to_img
from workflow import Workflow
import json

app = FastAPI()
GATEWAY_API_URL = 'http://127.0.0.1:5003/user_response'

class Image(BaseModel):
    distinct_id: int
    img: str
    lang: str


@app.post('/ocr', status_code=200)
def process_document(data: Image):
    processed_img = b64_to_img(data.img)

    worflow = Workflow(processed_img)
    results = worflow.run(data.lang)
    count = 0
    for batch in results:
        payload = {
            'distinct_id': data.distinct_id,
            'speech': batch,
        }
        with open(str(count) + 'audio.json', 'w') as f:
            json.dump(payload, f)

        process = multiprocessing.Pool(processes=1)
        process.apply_async(requests.post, [GATEWAY_API_URL, json.dumps(payload)])

        count += 1