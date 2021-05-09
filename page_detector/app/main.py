from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from page_detector import PageDetector
from utils import b64_to_img

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

    return jsonable_encoder(img_adjustments)

#curl -X POST "http://127.0.0.1:5001/page_position" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"distinct_id\":1000,\"img\":\"ss\",\"lang\":\"eng\"}"
