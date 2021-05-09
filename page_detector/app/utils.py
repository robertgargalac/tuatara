import cv2
import io
import numpy as np
from PIL import Image
from base64 import b64decode


def b64_to_img(base64_string):
    imgdata = b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
