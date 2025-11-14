import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK packages (first time only)
try:
    nltk.data.find("corpora/stopwords")
except:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except:
    nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def clean_text(text):

    # 1. Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()

    # 2. Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)

    # 3. Remove boilerplate news text patterns
    boilerplate_patterns = [
        r"subscribe now", r"read more", r"advertisement",
        r"all rights reserved", r"cookies", r"newsletter",
        r"click here", r"follow us", r"sign up"
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # 4. Remove duplicate lines
    lines = text.splitlines()
    unique_lines = list(dict.fromkeys(lines))  
    text = " ".join(unique_lines)

    # 5. Lowercasing
    text = text.lower()

    # 6. Remove numbers
    text = re.sub(r"\d+", "", text)

    # 7. Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 8. Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    # 9. Tokenization
    words = text.split()

    # 10. Stopword removal + Lemmatization
    final_words = [
        lemmatizer.lemmatize(w)
        for w in words
        if w not in stop_words and len(w) > 2
    ]

    # 11. Final clean text
    cleaned_text = " ".join(final_words)

    return cleaned_text
