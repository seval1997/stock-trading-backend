from flask import Blueprint, request, jsonify
from src.services.yfinance_service import YFinanceService

stock_bp = Blueprint("stock_api", __name__, url_prefix="/api/stocks")

# Dependency injection: swap YFinanceService with another implementation later
stock_service = YFinanceService()


@stock_bp.route("/<symbol>", methods=["GET"])
def get_stock_quote(symbol):
    try:
        data = stock_service.get_quote(symbol)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@stock_bp.route("/<symbol>/history", methods=["GET"])
def get_stock_history(symbol):
    period = request.args.get("period", "1mo")
    interval = request.args.get("interval", "1d")
    try:
        data = stock_service.get_history(symbol, period, interval)
        return jsonify({"symbol": symbol.upper(), "history": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@stock_bp.route("/search", methods=["GET"])
def search_stock():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter required"}), 400
    try:
        data = stock_service.search(query)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@stock_bp.route("/<symbol>/intraday", methods=["GET"])
def get_intraday(symbol):
    interval = request.args.get("interval", "1m")
    period = request.args.get("period", "1d")
    try:
        data = stock_service.get_intraday(symbol, interval, period)
        return jsonify({"symbol": symbol.upper(), "intraday": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
