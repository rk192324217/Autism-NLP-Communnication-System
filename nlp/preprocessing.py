import nltk
import string

# Ensure tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

from nltk.tokenize import word_tokenize


def tokenize(text):
    """
    Lowercase, remove punctuation, and tokenize text
    """
    if not text:
        return []

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)

    return tokens
