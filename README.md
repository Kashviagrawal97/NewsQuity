# NewsQuity - AI Equity Research Tool

NewsQuity is a fast, AI-powered equity research platform that stops you from reading 20 different news articles. It scans live market news, filters out duplicate hype, and delivers a clean, 10-second equity research summary with market sentiment and live TradingView charts.

## ✨ Features

- **Real-time News Aggregation**: Uses DuckDuckGo Search to fetch the latest news articles for any target stock.
- **Intelligent Web Scraping**: Extracts clean article text on the fly, bypassing clutter and ads.
- **Smart Deduplication**: Filters out repetitive news noise before AI processing.
- **AI Summarization & Sentiment**: Analyzes scraped text to extract key takeaways and determine market sentiment (Bullish/Bearish/Neutral).
- **Live Market Charts**: Integrated TradingView widget for real-time price tracking.
- **Report History**: SQLite caching to save and review past research reports instantly without re-running the AI.
- **Minimalist UI**: Built with Tailwind CSS for a professional, dark-themed financial dashboard experience.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Scraping**: DuckDuckGo Search (`duckduckgo-search`), BeautifulSoup4, Requests
- **AI Engine**: Google Gemini API, LangChain Core
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS, TradingView Lightweight Charts API

## 🚀 Setup & Installation (Local)

To get this project running on your local machine, run these commands in your terminal:

\`\`\`bash
# 1. Clone the repository
git clone https://github.com/yourusername/NewsQuity.git
cd NewsQuity

# 2. Create and activate the virtual environment
python3 -m venv NewsEquityVenv
source NewsEquityVenv/bin/activate   # (For Windows: NewsEquityVenv\Scripts\activate)

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Create a .env file and add your API key
echo "OPENAI_API_KEY=your_gemini_api_key_here" > .env
# Note: despite the variable name, this should be your Google Gemini API key

# 5. Run the application
uvicorn api:app --reload
\`\`\`

The app will be available at **http://localhost:8000**

## 🐳 Setup & Installation (Docker)

\`\`\`bash
# 1. Pull the image from Docker Hub
docker pull kashvibuilds/newsquity

# 2. Create a .env file in your working directory
echo "OPENAI_API_KEY=your_gemini_api_key_here" > .env

# 3. Run the container (maps port 8000 and injects your API key)
docker run -p 8000:8000 --env-file .env kashvibuilds/newsquity

# 4. Open the app
# Visit http://localhost:8000 in your browser
\`\`\`

> ⚠️ The `.env` file is intentionally **not** bundled inside the Docker image for security reasons. Every user running this image must supply their own `.env` file at runtime via `--env-file`, otherwise API calls will fail with a missing-key error.

## 📊 Usage

1. Enter a company/stock name in the search bar.
2. NewsQuity fetches recent news, scrapes full articles, removes duplicates, and generates an AI-powered summary with sentiment.
3. View the report alongside a live TradingView chart.
4. Past reports are cached in SQLite and viewable under report history.