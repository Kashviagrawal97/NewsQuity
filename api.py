"""
API layer - the ONLY file in this project that talks to the user.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database import init_db, get_reports_history
from pipeline import run_research


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # creates the SQLite tables on first run
    yield


app = FastAPI(title="Equity News Research Tool", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    company: str


@app.post("/research")
def research(request: ResearchRequest):
    """
    Takes a company name and returns a structured news report:
    summary, sentiment, key points, and source links.
    """
    return run_research(request.company)


@app.get("/history")
def history(limit: int = 20):
    """
    Returns recent historical equity reports stored in SQLite database.
    """
    return get_reports_history(limit=limit)


@app.get("/")
def serve_frontend():
    """
    Serves the frontend interface.
    """
    return FileResponse("index.html")