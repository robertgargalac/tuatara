import multiprocessing
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from utils import b64_to_img
app = FastAPI()

GATEWAY_API_URL = 'http://127.0.0.1:5003/user_response'

class Image(BaseModel):
    distinct_id: int
    img: str
    lang: str


@app.post('/ocr', status_code=200)
def get_page_position(data: Image):
    document = b64_to_img(data.img)

    results = worflow.run(document, data.language)

    for batch in results:
        payload = {
            'distinct_id': data.distinct_id,
            'speech': batch,
        }

        process = multiprocessing.Pool(processes=1)
        process.apply_async(requests.post, [GATEWAY_API_URL, payload])
