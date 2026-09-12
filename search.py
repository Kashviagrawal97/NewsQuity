"""
Discovery layer: finds candidate news articles for a company.

IMPORTANT: this only returns a title + url + short snippet for each
result - NOT the full article text. Getting the full article is
scraper.py's job, not this file's.
"""

from ddgs import DDGS

from config import MAX_SEARCH_RESULTS


def find_articles(company: str) -> list[dict]:
    """
    Searches DuckDuckGo's news index for a company and returns a list
    of {title, url, snippet} dicts - basically a search results page,
    not the articles themselves.
    """
    query = f"{company} stock news"
    results = DDGS().news(query=query, max_results=MAX_SEARCH_RESULTS)

    return [
        {
            "title": (r.get("title") or "").strip(),
            "url": (r.get("url") or "").strip(),
            "snippet": (r.get("body") or "").strip(),
        }
        for r in results
        if r.get("url")
    ]