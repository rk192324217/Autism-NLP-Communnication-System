import nltk
import re
from nltk.tokenize import word_tokenize

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def tokenize(text: str) -> list:
    if not text or not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if len(t) > 1]
    return tokens
