from abc import ABC, abstractmethod


class StockService(ABC):
    @abstractmethod
    def get_quote(self, symbol: str) -> dict:
        pass

    @abstractmethod
    def get_history(self, symbol: str, period: str, interval: str) -> list:
        pass

    @abstractmethod
    def search(self, query: str) -> dict:
        pass

    @abstractmethod
    def get_intraday(
        self, symbol: str, interval: str = "1m", period: str = "1d"
    ) -> list:
        pass
