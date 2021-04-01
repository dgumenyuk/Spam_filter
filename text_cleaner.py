import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextCleaning:
    """ Class to do text pre-processing and cleaning"""

    def remove_non_ascii(self, string):
        """ Returns the string without non ASCII characters"""
        stripped = (c for c in string if 0 < ord(c) < 127)
        return "".join(stripped)

    def remove_non_letters(self, string):
        string = re.sub(r"[^a-zA-Z]", " ", string)
        return string

    def stem_words(self, string):
        ps = PorterStemmer()
        string = [ps.stem(word) for word in string]
        return string

    def remove_stop_words(self, string):
        stop_words = set(stopwords.words("english"))
        string = [
            word for word in string if (word not in stop_words) and (len(word) > 2)
        ]
        return string

    def tokenize_words(self, string):
        return string.split()

    def clean_text(self, text):
        text = text.lower()
        text = self.remove_non_letters(text)
        text = self.remove_non_ascii(text)
        text = self.tokenize_words(text)
        text = self.remove_stop_words(text)
        text = self.stem_words(text)
        return text
