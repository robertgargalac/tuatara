import pytesseract
from pytesseract import Output
import cv2
from gtts import gTTS
import base64
import os
import re
import datefinder
from collections import defaultdict

from language_detector import LanguageDetector
from table_detection.model import Model
from items.document import Document
from items.utils import month_decode_dict


class Workflow:
    def __init__(self, image):
        """
        :param image: a gray image
        """
        self.image = image

    def run(self, language='english'):
        """
        :param language: 'english', 'romanian'
        :return:
        """
        tesseract_output = pytesseract.image_to_data(self.image, output_type=Output.DICT, lang='ron')

        self.date_processing(tesseract_output, language)

        lang_detector = LanguageDetector()
        doc = Document(self.image.shape[0], self.image.shape[1], lang_detector, language)
        doc.build_structure(tesseract_output)

        for p in doc.paragraph_objects:
            audio_binarry = self.text_to_speech(p.text)
            yield audio_binarry

    @staticmethod
    def text_to_speech(text, lang='en'):
        myobj = gTTS(text=text, lang=lang, slow=False)
        myobj.save('temp_file.mp3')

        f = open('temp_file.mp3', 'rb')
        enc = base64.b64encode(f.read())
        base64_message = enc.decode('ascii')

        os.remove('temp_file.mp3')
        return base64_message

    def date_processing(self, tesseract_output, language):
        max_dates = {}
        pos = {}
        for index, word in enumerate(tesseract_output['text']):
            if not word:
                continue
            date = self.normalize_dates(word, max_dates)
            if date:
                pos[index] = date

        # Figure out which index is month and which one is day
        if max_dates:
            month_index = min(max_dates, key=max_dates.get)

            for index in pos:
                date = pos[index]
                if date[month_index] in month_decode_dict[language].keys():
                    date[month_index] = month_decode_dict[language][date[month_index]]
                tesseract_output['text'][index] = ' '.join(date)

    @staticmethod
    def normalize_dates(word, max_dates):
        try:
            matches = datefinder.find_dates(word)
            date = next(matches)
        except:
            return

        divide = ['.', '/', '-']
        date_split = []
        for div in divide:
            match = re.search(r'(\d+{delim}\d+{delim}\d+)'.format(delim=div), word)
            if match:
                str_date = match.group(1)
                date_split = str_date.split(div)
                break

        for index, el in enumerate(date_split):
            if len(el) == 2:
                int_date = int(el)
                if index in max_dates.keys():
                    max_dates[index] = max(max_dates[index], int_date)
                else:
                    max_dates[index] = int_date
        return date_split
