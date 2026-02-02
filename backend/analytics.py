
import pandas as pd
import numpy as np

class PortfolioAnalytics:
    @staticmethod
    def calculate_returns(price_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates daily percentage returns.
        """
        return price_data.pct_change().dropna()

    @staticmethod
    def calculate_correlation_matrix(returns_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the Pearson correlation matrix.
        """
        return returns_data.corr()

    @staticmethod
    def calculate_volatility(returns_data: pd.DataFrame) -> pd.Series:
        """
        Calculates annualized volatility (standard deviation * sqrt(252)).
        """
        return returns_data.std() * np.sqrt(252)

    @staticmethod
    def portfolio_performance(weights: dict, returns_data: pd.DataFrame):
        """
        Calculates expected portfolio return and volatility.
        """
        # Align weights with available data
        tickers = list(weights.keys())
        available_tickers = [t for t in tickers if t in returns_data.columns]
        
        if not available_tickers:
            return 0.0, 0.0
            
        w = np.array([weights[t] for t in available_tickers])
        w = w / np.sum(w) # Normalize just in case
        
        mean_returns = returns_data.mean() * 252
        cov_matrix = returns_data.cov() * 252
        
        port_return = np.sum(mean_returns[available_tickers] * w)
        port_volatility = np.sqrt(np.dot(w.T, np.dot(cov_matrix.loc[available_tickers, available_tickers], w)))
        
        return port_return, port_volatility
