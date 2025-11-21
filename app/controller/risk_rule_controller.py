from flask import Blueprint, jsonify
from services.risk_rule_service import RiskRuleService

rule_bp = Blueprint("rules", __name__)

@rule_bp.get("/risk-rules")
def get_rules():
    return jsonify(RiskRuleService.get_all_rules())
