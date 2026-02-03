# Portfolio Correlation & Optimization Tool

A web-based application to analyze your investment portfolio, visualize correlations, and get AI-powered optimization advice.

## Features
- **Correlation Matrix**: Visualize how your assets move together.
- **Risk Metrics**: Calculate Volatility, Sharpe Ratio, and Expected Returns.
- **Optimization**: Get portfolio allocation suggestions using Mean-Variance Optimization (MVO) and Hierarchical Risk Parity (HRP).
- **AI Insights**: LLM-generated advice on diversification (requires OpenAI API).
- **Data Source**: Automatically fetches historical market data using `yfinance`.

## Prerequisites
- Python 3.8+
- Node.js 16+
- [OpenAI API Key](https://platform.openai.com/) (Optional)

## Setup & Run

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
# export OPENAI_API_KEY="your_key" # Optional

# OR For Ollama (Open Source)
export LLM_PROVIDER="ollama"
export LLM_MODEL="llama3" # or mistral, etc.
# export OLLAMA_BASE_URL="http://localhost:11434/v1" # Optional, default

uvicorn main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage
1. Open the frontend (usually `http://localhost:5173`).
2. Upload a CSV or Excel file with columns:
   - `Ticker` (e.g., AAPL)
   - `Weight` (Optional, e.g., 0.5)
3. View analysis and recommendations.
