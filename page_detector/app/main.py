import multiprocessing
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from page_detector import PageDetector
from utils import b64_to_img, img_to_b64

OCR_SERVICE_URL = 'http://127.0.0.1:5002/ocr'
app = FastAPI()
page_detector = PageDetector()


class Image(BaseModel):
    distinct_id: int
    img: str
    lang: str


@app.post('/page_position', status_code=200)
def get_page_position(data: Image):
    encoded_img = data.img
    decoded_img = b64_to_img(encoded_img)

    processed_img, img_adjustments = page_detector.process(decoded_img)

    if processed_img:
        processed_img_b64 = img_to_b64(processed_img)

        # Call ocr service
        payload = {
            'distinct_id': data.distinct_id,
            'img': processed_img_b64,
            'lang': data.lang
        }

        process = multiprocessing.Pool(processes=1)
        process.apply_async(requests.post, [OCR_SERVICE_URL, payload])

    return jsonable_encoder(img_adjustments)

#curl -X POST "http://127.0.0.1:5001/page_position" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"distinct_id\":1000,\"img\":\"ss\",\"lang\":\"eng\"}"
