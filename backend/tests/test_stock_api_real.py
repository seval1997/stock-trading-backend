import pytest
from flask import Flask
from src.api.stocks_api import stock_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(stock_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_stock_quote_real(client):
    resp = client.get("/api/stocks/AAPL")
    assert resp.status_code == 200
    data = resp.get_json()
    # yfinance returns live/delayed data, so just check keys exist
    assert data["symbol"] == "AAPL"
    assert "currentPrice" in data


def test_get_stock_history_real(client):
    resp = client.get("/api/stocks/AAPL/history?period=1mo&interval=1d")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "AAPL"
    assert isinstance(data["history"], list)
    assert len(data["history"]) > 0


def test_search_stock_real(client):
    resp = client.get("/api/stocks/search?query=MSFT")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "MSFT"
    assert "shortName" in data or "longName" in data


def test_get_intraday_real(client):
    resp = client.get("/api/stocks/AAPL/intraday?interval=1m&period=1d")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "AAPL"
    assert isinstance(data["intraday"], list)
    assert len(data["intraday"]) > 0
