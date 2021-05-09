class Document:
    def __init__(self, paragraphs, lines, words, w, h):
        self.paragraphs = paragraphs

        self.w = w
        self.h = h

    def filter_parapgrahs(self, lang):
        self.paragraphs = [
            paragraph
            for paragraph in self.paragraphs
            if paragraph.lang == lang
        ]
