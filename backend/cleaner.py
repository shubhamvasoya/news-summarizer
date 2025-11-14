import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK datasets are downloaded
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def clean_text(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+|https\S+", "", text)
    
    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)
    
    # Remove boilerplate text
    boilerplate_patterns = [
        r"subscribe.*?now",
        r"advertisement",
        r"all rights reserved",
        r"cookie.*?policy",
        r"newsletter.*?sign",
        r"click.*?here",
        r"read.*?more",
        r"share.*?article",
        r"follow.*?us",
    ]
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    # Remove numbers (if they don't add value)
    # Keep dates and important numbers by being selective
    text = re.sub(r"\b\d+(?:\s*(?:am|pm|am|pm))\b", "", text, flags=re.IGNORECASE)
    
    # Remove extra punctuation but keep sentence structure
    text = re.sub(r"[!?]{2,}", "!", text)  # Replace multiple ! or ? with single
    
    # Convert to lowercase
    text = text.lower()
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    # Tokenize into words
    words = text.split()
    
    # Remove stopwords and lemmatize
    cleaned_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words and len(word) > 2 and word.isalpha()
    ]
    
    return " ".join(cleaned_words)


def clean_text_for_display(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+|https\S+", "", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text
