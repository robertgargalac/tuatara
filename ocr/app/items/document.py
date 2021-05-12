from .base_item import BaseItem
from .paragraph import Paragraph
from .text_line import TextLine
from .utils import get_item


class Document:
    def __init__(self, w, h, lang_detector, preferred_language, multiple_lang_text=False):
        self.w = w
        self.h = h

        self.lang_detector = lang_detector
        self.preferred_language = preferred_language
        self.multiple_lang_text = multiple_lang_text

    def build_structure(self, tesseract_output):
        # Reformat the initial tesseract output
        paragraphs = get_item(tesseract_output, 'block_num')
        for p in paragraphs:
            p['lines'] = get_item(p, 'line_num')

        self.paragraph_objects = []

        for p in paragraphs:
            text_line_objects = []
            # Check paragraph's language
            text = ' '.join(p['text'])
            lang = self.lang_detector.get_language(text)
            if lang != self.preferred_language:
                continue

            for line in p['lines']:
                text_line = TextLine(
                    line['text'],
                    line['left'],
                    line['top'],
                    line['width'],
                    line['height'],
                )

                word_objects = []
                for index, word_text in enumerate(line['text']):
                    word = BaseItem(
                        word_text,
                        line['left'][index],
                        line['top'][index],
                        line['width'][index],
                        line['height'][index],
                    )
                    word_objects.append(word)

                text_line.words = word_objects
                text_line_objects.append(text_line)

            x1_list = [txt_line.x1 for txt_line in text_line_objects]
            x2_list = [txt_line.x2 for txt_line in text_line_objects]
            y1_list = [txt_line.y1 for txt_line in text_line_objects]
            y2_list = [txt_line.y2 for txt_line in text_line_objects]

            paragraph = Paragraph(
                p['text'],
                x1_list,
                y1_list,
                x2_list,
                y2_list,
                lang
            )
            paragraph.text_lines = text_line_objects
            self.paragraph_objects.append(paragraph)

    def filter_parapgrahs(self, lang):
        self.paragraphs = [
            paragraph
            for paragraph in self.paragraphs
            if paragraph.lang == lang
        ]
