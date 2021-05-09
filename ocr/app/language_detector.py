from nltk import word_tokenize
from nltk.corpus import stopwords

NLTK_LANG = stopwords.fileids()  # list of languages which have stopwords in nltk


class LanguageDetector:
    def __init__(self):
        self.stopwords_counter = {}

    def get_language(self, text):
        tokens = word_tokenize(text)
        lowered_tokens = set([token.lower() for token in tokens])

        for lang in NLTK_LANG:
            lang_stopwords = set(stopwords.words(lang))
            common_words = lowered_tokens.intersection(lang_stopwords)

            self.stopwords_counter[lang] = len(common_words)

        detected_language = max(self.stopwords_counter.items(), key=lambda x: x[1])[0]
        return detected_language
