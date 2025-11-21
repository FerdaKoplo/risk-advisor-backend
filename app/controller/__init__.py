from flask import Blueprint
from .ai_controller import ai_route
from .risk_controller import risk_bp 
from .risk_rule_controller import rule_bp
from .risk_trend_controller import trend_bp
from .risk_factors_controller import risk_factors_bp

api = Blueprint('api', __name__)

api.register_blueprint(risk_factors_bp)
api.register_blueprint(ai_route)
api.register_blueprint(risk_bp)
api.register_blueprint(rule_bp)
api.register_blueprint(trend_bp)
