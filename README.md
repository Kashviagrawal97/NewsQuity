# 📈 NewsQuity - AI Equity Research Tool

NewsQuity is a fast, AI-powered equity research platform that stops you from reading 20 different news articles. It scans live market news, filters out duplicate hype, and delivers a clean, 10-second equity research summary with market sentiment and live TradingView charts.

## ✨ Features
* **Real-time News Aggregation:** Uses DuckDuckGo Search to fetch the latest news articles for any target stock.
* **Intelligent Web Scraping:** Extracts clean article text on the fly, bypassing clutter and ads.
* **Smart Deduplication:** Filters out repetitive news noise before AI processing.
* **AI Summarization & Sentiment:** Analyzes scraped text to extract key takeaways and determine market sentiment (Bullish/Bearish/Neutral).
* **Live Market Charts:** Integrated TradingView widget for real-time price tracking.
* **Report History:** SQLite caching to save and review past research reports instantly without re-running the AI.
* **Minimalist UI:** Built with Tailwind CSS for a professional, dark-themed financial dashboard experience.

## 🛠️ Tech Stack

* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **Scraping:** DuckDuckGo Search (`duckduckgo-search`), BeautifulSoup4, Requests
* **AI Engine:** Google GenAI API (Gemini), LangChain Core
* **Database:** SQLite
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS, TradingView Lightweight Charts API

---

## 🚀 Setup & Installation

To get this project running on your local machine, simply run these commands in your terminal:

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/NewsQuity.git](https://github.com/yourusername/NewsQuity.git)
cd NewsQuity

# 2. Create and activate the Virtual Environment
python3 -m venv NewsEquityVnev
source NewsEquityVenv/bin/activate  # (For Windows: NewsEquityVenv\Scripts\activate)

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Create a .env file and add your API key (Replace with your actual key)
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# 5. Run the application
uvicorn api:app --reload
