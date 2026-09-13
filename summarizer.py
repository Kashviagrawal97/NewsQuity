"""
LLM layer: takes a list of cleaned articles and produces a structured
report (summary, sentiment, key points) using LangChain.
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

REPORT_PROMPT = ChatPromptTemplate.from_template("""
You are an equity research assistant. Based only on the news articles
below about {company}, produce a JSON object with these exact keys:

- "summary": a 3-4 sentence overview of what's happening with the company
- "sentiment": one of "bullish", "bearish", or "neutral"
- "key_points": a list of 3-5 short bullet points on the most important events

Articles:
{articles_text}

Respond with ONLY the JSON object, no other text.
""")


def _build_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0,
        api_key = os.getenv("OPENAI_API_KEY"),
    )

def generate_report(company: str, articles: list[dict]) -> dict:
    """
    Feeds all article contents to the LLM in one prompt and asks for a
    structured JSON report back. Attaches the source URLs afterward so
    the final report can be traced back to where it came from.
    """
    articles_text = "\n\n".join(
        f"Title: {a['title']}\n"
        f"Date: {a.get('published_date', 'unknown')}\n"
        f"Content: {a['content'][:1500]}"  # cap length per article to control cost
        for a in articles
    )

    chain = REPORT_PROMPT | _build_llm() | JsonOutputParser()
    result = chain.invoke({"company": company, "articles_text": articles_text})

    result["sources"] = [a["url"] for a in articles]
    return result