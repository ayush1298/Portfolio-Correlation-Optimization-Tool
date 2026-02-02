
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions
from pypfopt import HRPOpt

class PortfolioOptimizer:
    def __init__(self, price_data: pd.DataFrame):
        self.prices = price_data
        
    def optimize_efficient_frontier(self, risk_aversion: float = 1.0) -> dict:
        """
        Optimizes for standard Mean-Variance Optimization (Max Sharpe by default).
        """
        if self.prices.empty:
            return {}
            
        # Calculate expected returns and sample covariance
        mu = expected_returns.mean_historical_return(self.prices)
        S = risk_models.sample_cov(self.prices)

        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        
        # Add regularization (optional but good for stability)
        # ef.add_objective(objective_functions.L2_reg, gamma=0.1)
        
        try:
            raw_weights = ef.max_sharpe()
            cleaned_weights = ef.clean_weights()
            return cleaned_weights
        except Exception as e:
            print(f"Optimization failed: {e}")
            return {}

    def optimize_hrp(self) -> dict:
        """
        Hierarchical Risk Parity optimization.
        Robust to noise and doesn't require covariance matrix inversion.
        """
        if self.prices.empty:
            return {}
            
        returns = self.prices.pct_change().dropna()
        hrp = HRPOpt(returns)
        
        try:
            raw_weights = hrp.optimize()
            cleaned_weights = hrp.clean_weights()
            return cleaned_weights
        except Exception as e:
            print(f"HRP Optimization failed: {e}")
            return {}
