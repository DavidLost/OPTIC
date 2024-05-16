from bs4 import BeautifulSoup
import requests
from langdetect import detect, DetectorFactory
import langcodes

# Set seed to ensure reproducibility
DetectorFactory.seed = 0

def fetch_headers(url: str) -> dict:
    """
    Fetches the headers from the given URL.
    
    Parameters:
    url (str): The URL to fetch headers from.
    
    Returns:
    dict: The headers of the response.
    """
    try:
        response = requests.head(url)
        response.raise_for_status()
        return response.headers
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        return {}

def extract_text_from_url(url: str) -> str:
    """
    Extracts and returns all text from the given URL.
    
    Parameters:
    url (str): The URL to fetch content from.
    
    Returns:
    str: The extracted text content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

def detect_language(text: str) -> str:
    """
    Detects the language of the given text.
    
    Parameters:
    text (str): The text to detect the language of.
    
    Returns:
    str: The detected language code (e.g., 'en' for English, 'de' for German).
    """
    try:
        return detect(text)
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "unknown"

def get_language_name(lang_code: str) -> str:
    """
    Converts a language code to the full language name.
    
    Parameters:
    lang_code (str): The language code (e.g., 'en').
    
    Returns:
    str: The full language name (e.g., 'English').
    """
    try:
        language = langcodes.Language.get(lang_code)
        return language.language_name()
    except Exception as e:
        print(f"Error converting language code to name: {e}")
        return "unknown"

def get_language_from_headers(headers: dict) -> str:
    """
    Retrieves the language from the headers if available.
    
    Parameters:
    headers (dict): The headers to check for the Content-Language.
    
    Returns:
    str: The language code if found, else an empty string.
    """
    return headers.get('Content-Language', '')

def get_language_from_html(soup: BeautifulSoup) -> str:
    """
    Retrieves the language from the HTML tag if available.
    
    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object of the webpage.
    
    Returns:
    str: The language code if found, else an empty string.
    """
    html_tag = soup.find('html')
    if html_tag and html_tag.has_attr('lang'):
        return html_tag['lang']
    return ''

def determine_language(url: str) -> str:
    """
    Determines the language of a website using headers, HTML, or text analysis.
    
    Parameters:
    url (str): The URL of the website.
    
    Returns:
    str: The full language name and code.
    """
    # Check headers for language
    headers = fetch_headers(url)
    language_code = get_language_from_headers(headers)
    if language_code:
        print(f'lang ({language_code}) was found by headers')
        return get_language_name(language_code)

    # Check HTML tag for language
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        language_code = get_language_from_html(soup)
        if language_code:
            print(f'lang ({language_code}) was found by html tag')
            return get_language_name(language_code)
        
        # Fallback to text analysis
        language_code = detect_language(soup.get_text())
        print(f'lang ({language_code}) was found by text analysis')
        return get_language_name(language_code)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return "unknown"