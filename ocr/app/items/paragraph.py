from base_item import BaseItem


class Paragraph(BaseItem):
    def __init__(self, text, x1, y1, x2, y2, lang, text_lines=None):
        super().__init__(text, x1, y1, x2, y2)
        self.text = ' '.join(text)
        self.lang = lang
        self.text_lines = text_lines

    def compute_coordinates(self, x1,  y1, x2, y2):
        x1 = min(x1)
        y1 = min(y1)

        x2 = max(x2)
        y2 = max(y2)
        return x1, y1, x2, y2