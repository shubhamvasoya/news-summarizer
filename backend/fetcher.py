import requests
from bs4 import BeautifulSoup

def extract_article_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Prefer <article> tag if available
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = article_tag.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        # Extract paragraph text
        text = " ".join([p.get_text(separator=" ", strip=True) for p in paragraphs])

        # Return None if text too short (likely invalid)
        if len(text) < 80:
            return None

        return text

    except Exception as e:
        print("Error extracting article:", e)
        return None
