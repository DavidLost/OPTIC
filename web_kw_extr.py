from bs4 import BeautifulSoup
import requests

DEFAULT_MIN_LEN = 4

def extract_keywords(url: str, min_len: int = DEFAULT_MIN_LEN):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return {word for word in soup.get_text().split() if len(word) >= min_len}