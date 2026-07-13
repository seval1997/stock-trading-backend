import yfinance as yf
from .stock_service import StockService


class YFinanceService(StockService):
    def get_quote(self, symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol.upper(),
            "currentPrice": info.get("currentPrice"),
            "previousClose": info.get("previousClose"),
            "open": info.get("open"),
            "dayHigh": info.get("dayHigh"),
            "dayLow": info.get("dayLow"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
        }

    def get_history(self, symbol: str, period: str, interval: str) -> list:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        return hist.reset_index().to_dict(orient="records")

    def search(self, query: str) -> dict:
        ticker = yf.Ticker(query)
        info = ticker.info
        return {
            "symbol": query.upper(),
            "shortName": info.get("shortName"),
            "longName": info.get("longName"),
            "exchange": info.get("exchange"),
            "currency": info.get("currency"),
        }

    def get_intraday(
        self, symbol: str, interval: str = "1m", period: str = "1d"
    ) -> list:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        return hist.reset_index().to_dict(orient="records")
