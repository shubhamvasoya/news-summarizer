import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def is_valid_url(url):
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_article_from_url(url):
    
    if not is_valid_url(url):
        print(f"Invalid URL format: {url}")
        return None
    
    try:
        # Set user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Fetch the webpage with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Try to find article tag first (most semantic)
        article_tag = soup.find("article")
        
        if article_tag:
            paragraphs = article_tag.find_all("p")
        else:
            # Fallback to main or body
            main_tag = soup.find("main")
            if main_tag:
                paragraphs = main_tag.find_all("p")
            else:
                paragraphs = soup.find_all("p")
        
        # Extract text from paragraphs
        text = " ".join([
            p.get_text(separator=" ", strip=True)
            for p in paragraphs
        ])
        
        # Clean up excessive whitespace
        text = " ".join(text.split())
        
        # Minimum valid content check (at least 80 characters)
        if len(text) > 80:
            return text
        else:
            print("Article text too short for summarization")
            return None
    
    except requests.exceptions.Timeout:
        print("Error: Request timed out while fetching the URL")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the URL")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None
