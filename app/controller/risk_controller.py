from flask import Blueprint, request, jsonify
from app.services.risk_service import RiskService

risk_bp = Blueprint("risk", __name__)

@risk_bp.post("/calculate")
def calculate_risk():
    data = request.json
    result = RiskService.create_assessment(data)
    return jsonify(result), 201
