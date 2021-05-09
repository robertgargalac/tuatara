from .base_item import BaseItem


class Paragraph(BaseItem):
    def __init__(self, text, x, y, w, h, lang, lines=None):
        super().__init__(text, x, y, w, h)
        self.text = ' '.join(text)
        self.lang = lang
        self.lines = lines

    def compute_coordinates(self, x,  y, w, h):
        x1 = min(x)
        y1 = min(y)

        total_height = max(h)
        total_width = sum(w)

        x2 = x1 + total_width
        y2 = y1 + total_height
        return x1, y1, x2, y2