from flask import Blueprint, jsonify
from app.services.risk_trend_service import RiskTrendService

trend_bp = Blueprint("trend", __name__)

@trend_bp.get("/trend/daily")
def trend_daily():
    return jsonify(RiskTrendService.daily_trend(7))

@trend_bp.get("/trend/monthly")
def trend_monthly():
    return jsonify(RiskTrendService.monthly_trend(6))