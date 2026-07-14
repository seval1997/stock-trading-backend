import pytest
from flask import Flask
from src.api.stocks_api import stock_bp


# --- Fixtures ---
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(stock_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# --- Mock Service ---
class MockService:
    def get_quote(self, symbol):
        return {"symbol": symbol.upper(), "currentPrice": 123.45}

    def get_history(self, symbol, period, interval):
        return [{"Date": "2026-07-13", "Open": 100, "Close": 110}]

    def search(self, query):
        return {"symbol": query.upper(), "shortName": "Mock Corp"}

    def get_intraday(self, symbol, interval, period):
        return [{"Datetime": "2026-07-13T09:30:00", "Open": 100, "Close": 105}]


# --- Patch stock_service ---
@pytest.fixture(autouse=True)
def patch_service(monkeypatch):
    from src.api import stocks_api

    stocks_api.stock_service = MockService()


# --- Tests ---
def test_get_stock_quote(client):
    resp = client.get("/api/stocks/AAPL")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "AAPL"
    assert "currentPrice" in data


def test_get_stock_history(client):
    resp = client.get("/api/stocks/AAPL/history?period=1mo&interval=1d")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "AAPL"
    assert isinstance(data["history"], list)
    assert "Open" in data["history"][0]


def test_search_stock(client):
    resp = client.get("/api/stocks/search?query=MSFT")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "MSFT"
    assert data["shortName"] == "Mock Corp"


def test_search_stock_missing_query(client):
    resp = client.get("/api/stocks/search")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_get_intraday(client):
    resp = client.get("/api/stocks/AAPL/intraday?interval=1m&period=1d")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "AAPL"
    assert isinstance(data["intraday"], list)
    assert "Open" in data["intraday"][0]
