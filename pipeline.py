"""
Orchestrates the full flow: search -> scrape -> dedup -> save -> summarize.

api.py calls ONLY this file. It never talks to search.py, scraper.py,
database.py, or summarizer.py directly - that's the whole point of
keeping api.py a thin input/output layer.
"""

from config import CACHE_FRESHNESS_HOURS
from database import (
    get_existing_titles,
    get_recent_articles,
    save_article,
    save_report,
)
from dedup import deduplicate
from scraper import extract_article
from search import find_articles
from summarizer import generate_report


def run_research(company: str) -> dict:
    """
    Runs the full pipeline for one company and returns a structured
    report. Reuses recently cached articles instead of re-scraping
    when a fresh-enough copy already exists.
    """
    articles_to_summarize = get_recent_articles(company, hours=CACHE_FRESHNESS_HOURS)

    if not articles_to_summarize:
        search_results = find_articles(company)

        scraped = []
        for result in search_results:
            article = extract_article(result["url"])
            if article:
                scraped.append(article)

        existing_titles = get_existing_titles(company)
        new_articles = deduplicate(scraped, existing_titles)

        for article in new_articles:
            save_article(company, article)

        articles_to_summarize = new_articles or scraped

    if not articles_to_summarize:
        return {
            "company": company,
            "summary": "No recent news articles could be found or read for this company.",
            "sentiment": "neutral",
            "key_points": [],
            "sources": [],
        }

    report = generate_report(company, articles_to_summarize)
    report["company"] = company

    save_report(company, report)
    return report