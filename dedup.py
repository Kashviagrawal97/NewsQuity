"""
Removes duplicate / near-duplicate articles by comparing titles.
Pure Python (difflib) - no extra library needed for this.
"""

from difflib import SequenceMatcher

from config import DEDUP_SIMILARITY_THRESHOLD


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate(articles: list[dict], already_seen_titles: list[str]) -> list[dict]:
    """
    Given freshly scraped articles and a list of titles already stored
    for this company, returns only the articles that are genuinely new -
    not near-duplicates of each other or of what's already saved.
    """
    unique_articles: list[dict] = []
    seen_titles = list(already_seen_titles)

    for article in articles:
        title = article["title"]
        is_duplicate = any(
            _similarity(title, seen) > DEDUP_SIMILARITY_THRESHOLD
            for seen in seen_titles
        )
        if not is_duplicate:
            unique_articles.append(article)
            seen_titles.append(title)

    return unique_articles