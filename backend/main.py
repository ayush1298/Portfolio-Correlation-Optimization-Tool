from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .data_loader import DataLoader
from .analytics import PortfolioAnalytics
from .optimizer import PortfolioOptimizer
from .llm_advisor import LLMAdvisor
import pandas as pd
from typing import Dict, Any
import io

app = FastAPI(title="Portfolio Correlation Optimization Tool")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Portfolio Optimization API"}

@app.post("/api/analyze")
async def analyze_portfolio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    contents = await file.read()
    loader = DataLoader()
    
    try:
        # Load Portfolio
        portfolio_df = loader.load_portfolio_from_file(contents, file.filename)
        
        # Validate Columns
        df_cols = portfolio_df.columns.tolist()
        
        # Check if 'ticker' exists, otherwise look for 'company'/'name'
        if 'ticker' not in df_cols:
            name_col = next((c for c in df_cols if c in ['company', 'name', 'description', 'security']), None)
            if name_col:
                # Resolve Tickers
                print("Resolving tickers from company names...")
                resolved_tickers = []
                for name in portfolio_df[name_col]:
                    ticker = loader.resolve_ticker(name)
                    if ticker:
                        resolved_tickers.append(ticker)
                    else:
                        raise HTTPException(status_code=400, detail=f"Could not resolve ticker for: {name}")
                portfolio_df['ticker'] = resolved_tickers
            else:
                 raise HTTPException(status_code=400, detail="File must contain a 'Ticker' or 'Company' column.")

        tickers = portfolio_df['ticker'].tolist()
        
        # Extract weights if available, else equal weight
        if 'weight' in portfolio_df.columns:
            weights = dict(zip(portfolio_df['ticker'], portfolio_df['weight']))
        elif 'quantity' in portfolio_df.columns:
            # We can't determine weight without price, so strictly we need fetching first
            # but for now let's assume we proceed to fetch
            weights = {} 
        else:
            weights = {t: 1.0/len(tickers) for t in tickers}
            
        # Fetch Market Data
        price_data = loader.fetch_market_data(tickers)
        
        if price_data.empty:
            raise HTTPException(status_code=400, detail="Could not fetch market data. Check API key or Tickers.")

        # Calculate Analytics
        returns_data = PortfolioAnalytics.calculate_returns(price_data)
        corr_matrix = PortfolioAnalytics.calculate_correlation_matrix(returns_data)
        volatility = PortfolioAnalytics.calculate_volatility(returns_data)
        
        # Current Performance (if weights exist)
        current_perf = {}
        if weights:
            ret, vol = PortfolioAnalytics.portfolio_performance(weights, returns_data)
            current_perf = {"return": ret, "volatility": vol, "sharpe": ret/vol if vol != 0 else 0}

        # Optimization
        optimizer = PortfolioOptimizer(price_data)
        mvo_weights = optimizer.optimize_efficient_frontier()
        hrp_weights = optimizer.optimize_hrp()
        
        # LLM Advice
        advisor = LLMAdvisor()
        advice = advisor.get_portfolio_advice(
            {"tickers": tickers, "weights": weights},
            current_perf,
            {"mvo": mvo_weights, "hrp": hrp_weights}
        )
        
        return {
            "tickers": tickers,
            "correlation_matrix": corr_matrix.to_dict(),
            "volatility": volatility.to_dict(),
            "current_performance": current_perf,
            "optimized_weights": {
                "mvo": mvo_weights,
                "hrp": hrp_weights
            },
            "llm_advice": advice
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
