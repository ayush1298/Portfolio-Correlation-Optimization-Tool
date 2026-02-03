
import pandas as pd
import numpy as np
import yfinance as yf
import os
from typing import List, Dict, Optional
from io import BytesIO

class DataLoader:
    def __init__(self, api_key: str = None):
        # API Key not needed for yfinance, but kept for interface consistency
        self.api_key = api_key

    def load_portfolio_from_file(self, content: bytes, filename: str) -> pd.DataFrame:
        """
        Parses an uploaded Excel or CSV file.
        Expected columns: 'Ticker', 'Weight' (optional), or 'Quantity'
        """
        if filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(content))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(BytesIO(content))
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")
        
        # Normalize columns
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Check required columns
        if 'ticker' not in df.columns:
            raise ValueError("File must contain a 'Ticker' column. Ticker resolution is currently disabled.")
            
        return df

    def fetch_market_data(self, tickers: List[str], period: str = '1y') -> pd.DataFrame:
        """
        Fetches historical adjusted close prices for the given tickers using yfinance.
        """
        combined_df = pd.DataFrame()
        
        if not tickers:
            return combined_df
            
        try:
            # yfinance allows bulk download
            data = yf.download(tickers, period=period, auto_adjust=True)
            
            # yf.download returns a MultiIndex if multiple tickers
            if len(tickers) > 1:
                # We want 'Close' or 'Adj Close' (auto_adjust=True gives 'Close' as adjusted)
                if 'Close' in data.columns:
                    combined_df = data['Close']
                else:
                    # Fallback if structure is different
                    combined_df = data
            else:
                # Single ticker
                if 'Close' in data.columns:
                    combined_df = pd.DataFrame({tickers[0]: data['Close']})
                else:
                    combined_df = data        
        
        except Exception as e:
            print(f"Error fetching data with yfinance: {e}")
            
        return combined_df

    def resolve_ticker(self, company_name: str) -> Optional[str]:
        """
        Ticker resolution is disabled with yfinance as it doesn't provide a reliable search API.
        """
        print(f"Ticker resolution disabled. Cannot resolve: {company_name}")
        return None

