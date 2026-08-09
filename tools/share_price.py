from langchain_core.tools import tool



@tool
def get_share_price(symbol: str) -> float:
    """Return the current share price for a given ticker symbol."""
    fake_prices = {"AAPL": 241.5, "GOOG": 168.2, "AMZN": 198.0}
    return fake_prices.get(symbol.upper(), 0.0)

