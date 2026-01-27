import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

def tokenize(text):
    text = clean_text(text)
    return word_tokenize(text)
