from .base_item import BaseItem


class TextLine(BaseItem):
    def __init__(self, text, x, y, w, h, words=None):
        super().__init__(text, x, y, w, h)
        self.text = ' '.join(text)
        self.words = words

    def compute_coordinates(self, x,  y, w, h):
        x1 = min(x)
        y1 = min(y)

        last_height = h[-1]
        last_width = w[-1]

        x2 = x[-1] + last_width
        y2 = y[-1] + last_height
        return x1, y1, x2, y2


