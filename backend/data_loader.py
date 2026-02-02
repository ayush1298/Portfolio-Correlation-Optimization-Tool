
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import os
from typing import List, Dict, Optional
from io import BytesIO

class DataLoader:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            # Fallback or warning - for now we might raise an error if strictly required
            # But let's allow it to be None for CSV-only usage if possible, 
            # though the plan implies we need market data.
            pass
        self.ts = TimeSeries(key=self.api_key, output_format='pandas') if self.api_key else None

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
            raise ValueError("File must contain a 'Ticker' column.")
            
        return df

    def fetch_market_data(self, tickers: List[str], period: str = '1Y') -> pd.DataFrame:
        """
        Fetches historical adjusted close prices for the given tickers.
        Note: Alpha Vantage free tier has rate limits (5 calls/min, 500/day).
        We should handle this carefully or mock for testing.
        """
        if not self.ts:
            raise ValueError("Alpha Vantage API key is missing.")

        combined_df = pd.DataFrame()
        
        # Simple implementation - needs more robust error handling / rate limiting for prod
        for ticker in tickers:
            try:
                # Get daily adjusted close prices
                data, meta_data = self.ts.get_daily_adjusted(symbol=ticker, outputsize='full')
                
                # Filter by simple logic or just take last N days based on 'period'
                # For simplicity, let's take all and filter later, or just last year
                # Note: Alpha Vantage 'full' returns 20 years. 'compact' returns 100 days.
                
                # Extract '5. adjusted close'
                close_series = data['5. adjusted close']
                close_series.name = ticker
                
                if combined_df.empty:
                    combined_df = pd.DataFrame(close_series)
                else:
                    combined_df = combined_df.join(close_series, how='outer')
                    
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                
        # Limit to requested period (approximate 1Y = 252 trading days)
        # This implementation is basic.
        if not combined_df.empty:
            combined_df = combined_df.sort_index(ascending=True)
            if period == '1Y':
                combined_df = combined_df.tail(252)
        
        return combined_df

    def resolve_ticker(self, company_name: str) -> Optional[str]:
        """
        Searches for a ticker symbol given a company name using Alpha Vantage API.
        """
        if not self.api_key:
            return None
            
        import requests
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={self.api_key}"
        try:
            r = requests.get(url)
            data = r.json()
            matches = data.get("bestMatches", [])
            if matches:
                # Return the symbol of the first (best) match
                return matches[0]["1. symbol"]
        except Exception as e:
            print(f"Error resolving ticker for {company_name}: {e}")
            
        return None
