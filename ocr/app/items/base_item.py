class BaseItem:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x1, self.y1, self.x2, self.y2 = self.compute_coordinates(x, y, w, h)

    def compute_coordinates(self, x, y, w, h):
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        return x1, y1, x2, y2
