"""
Handles all SQLite reads/writes. No other file should touch the
database directly - they call functions from here instead.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

from config import DB_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Creates the tables if they don't exist yet. Safe to call every startup."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                published_date TEXT,
                content TEXT,
                scraped_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                summary TEXT,
                sentiment TEXT,
                key_points TEXT,
                sources TEXT,
                created_at TEXT NOT NULL
            )
        """)


def get_existing_titles(company: str) -> list[str]:
    """Titles already stored for this company - used by dedup.py to spot repeats."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT title FROM articles WHERE company = ?", (company,)
        ).fetchall()
        return [row["title"] for row in rows]


def save_article(company: str, article: dict):
    """Saves one scraped article. Silently skips it if the URL is already stored."""
    with get_connection() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO articles
                (company, title, url, published_date, content, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company,
            article["title"],
            article["url"],
            article.get("published_date"),
            article.get("content"),
            datetime.utcnow().isoformat() + "Z",
        ))


def get_recent_articles(company: str, hours: int) -> list[dict]:
    """Articles scraped within the last `hours` - lets the pipeline skip re-scraping."""
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT title, url, published_date, content FROM articles
            WHERE company = ? AND scraped_at >= ?
        """, (company, cutoff)).fetchall()
        return [dict(row) for row in rows]


def save_report(company: str, report: dict):
    """Stores a generated report so sentiment history can be reviewed later."""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO reports
                (company, summary, sentiment, key_points, sources, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company,
            report.get("summary", ""),
            report.get("sentiment", ""),
            "|".join(report.get("key_points", [])),
            "|".join(report.get("sources", [])),
            datetime.utcnow().isoformat() + "Z",
        ))


def get_reports_history(limit: int = 20) -> list[dict]:
    """Fetches previously saved reports ordered by most recent first."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, company, summary, sentiment, key_points, sources, created_at
            FROM reports
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        history = []
        for row in rows:
            r = dict(row)
            kp_raw = r.get("key_points") or ""
            src_raw = r.get("sources") or ""
            r["key_points"] = [kp for kp in kp_raw.split("|") if kp]
            r["sources"] = [src for src in src_raw.split("|") if src]
            history.append(r)
        return history