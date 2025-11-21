from flask import Blueprint, jsonify
from app.models import RiskFactorDefinition 

risk_factors_bp = Blueprint("risk_factors", __name__)

@risk_factors_bp.get("/risk-factors")
def get_risk_factors():
    factors = RiskFactorDefinition.query.all()
    return jsonify([{
        "factor_id": f.factor_id,
        "label": f.label,
        "weights": f.weights
    } for f in factors])
