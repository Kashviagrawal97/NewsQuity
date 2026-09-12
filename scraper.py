"""
Extraction layer: given a single URL, fetches the page and pulls out
the full article title, published date, and body text.

This is the step search.py cannot do - DuckDuckGo only hands back a
short preview snippet, not the whole article.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (equity-research-bot/1.0)"}
TIMEOUT = 10
MIN_CONTENT_LENGTH = 200  # below this, the page probably didn't load properly


def extract_article(url: str) -> dict | None:
    """
    Fetches a URL and extracts title, date, and body text.

    Returns None if the page can't be fetched or doesn't contain enough
    readable text - the caller just skips that source rather than crash.
    A None result on a JS-heavy site is exactly where you'd plug in a
    Selenium-based fallback later.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    content = _get_body_text(soup)
    if len(content) < MIN_CONTENT_LENGTH:
        return None

    return {
        "title": _get_title(soup),
        "url": url,
        "published_date": _get_date(soup),
        "content": content,
    }


def _get_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else "Untitled"


def _get_date(soup: BeautifulSoup) -> str | None:
    # Most news sites expose the publish date in a <time> tag or a meta tag
    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        return time_tag["datetime"]

    meta_date = soup.find("meta", attrs={"property": "article:published_time"})
    if meta_date and meta_date.get("content"):
        return meta_date["content"]

    return None


def _get_body_text(soup: BeautifulSoup) -> str:
    paragraphs = soup.find_all("p")
    return " ".join(p.get_text(strip=True) for p in paragraphs).strip()