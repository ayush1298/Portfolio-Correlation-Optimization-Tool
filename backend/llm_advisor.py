
import os
from openai import OpenAI
import json

class LLMAdvisor:
    def __init__(self, api_key: str = None, provider: str = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        # If openai, key comes from arg or env. If ollama, key is 'ollama' or ignored.
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-4o" if self.provider == "openai" else "llama3")

        if self.provider == "ollama":
            self.client = OpenAI(base_url=self.base_url, api_key="ollama")
        elif self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def get_portfolio_advice(self, current_portfolio: dict, metrics: dict, optimized_weights: dict) -> str:
        """
        Generates advice based on portfolio data.
        """
        if not self.client:
            return "LLM Advisor disabled (API Key missing or provider not configured)."
            
        prompt = self._construct_prompt(current_portfolio, metrics, optimized_weights)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial advisor. Analyze the portfolio metrics and optimization suggestions provided. Give concise, actionable advice on how to improve the portfolio's risk-adjusted return. Focus on diversification gaps."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error gathering advice: {str(e)}"

    def _construct_prompt(self, current_portfolio, metrics, optimized_weights) -> str:
        return f"""
        Current Portfolio Tickers: {current_portfolio.get('tickers', [])}
        
        Current Performance:
        - Annual Return: {metrics.get('return', 0):.2%}
        - Volatility: {metrics.get('volatility', 0):.2%}
        - Sharpe Ratio: {metrics.get('sharpe', 0):.2f}
        
        Optimization Suggestion (MVO):
        {json.dumps(optimized_weights.get('mvo', {}), indent=2)}
        
        Optimization Suggestion (HRP):
        {json.dumps(optimized_weights.get('hrp', {}), indent=2)}
        
        Please compare the current portfolio with the optimized suggestions and explain 3 key changes the user should make.
        """
