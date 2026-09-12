"""
Central place for settings so nothing is hardcoded across files.
"""

# SQLite database file (created automatically on first run)
DB_PATH = "equity_research.db"

# How many articles to try pulling per company from search
MAX_SEARCH_RESULTS = 8

# How similar two titles must be (0-1) to be treated as duplicates
DEDUP_SIMILARITY_THRESHOLD = 0.85

# If we already scraped this company recently, reuse those articles
# instead of scraping again
CACHE_FRESHNESS_HOURS = 12

