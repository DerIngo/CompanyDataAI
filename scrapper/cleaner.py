import re
import unicodedata
from bs4 import BeautifulSoup
from langdetect import detect

def remove_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=" ").strip()

def remove_extra_whitespace(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def remove_boilerplate(text):
    boilerplate_patterns = [
        r'Copyright\s+\d{4}',  
        r'All rights reserved',
        r'Terms of Service|Privacy Policy',
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text.strip()

def normalize_text(text):
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if c.isprintable())

def filter_by_language(text, target_language='de'):
    try:
        if detect(text) == target_language:
            return text
    except Exception:
        pass
    return ""

def clean_html_content(html_content, target_language='de'):
    text = remove_html_tags(html_content)
    text = remove_extra_whitespace(text)
    text = remove_boilerplate(text)
    text = normalize_text(text)
    text = filter_by_language(text, target_language=target_language)
    return text
