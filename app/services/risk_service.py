from models.risk_assesment import RiskAssessment
from models.risk_factor_definitions import RiskFactorDefinition
from models.risk_matrix_rule import RiskMatrixRule
from extension import db
from datetime import datetime


class RiskService:
    @staticmethod
    def calculate_score(prob_weight: int, sev_weight: int, comp_multiplier: float) -> int:
        return int((prob_weight * sev_weight) * comp_multiplier)

    @staticmethod
    def get_weights(factor_id: str, input_option: str) -> float:
        factor = RiskFactorDefinition.query.filter_by(factor_id=factor_id).first()

        if not factor:
            raise ValueError(f"Risk factor '{factor_id}' tidak ditemukan")

        weights = factor.weights

        if input_option not in weights:
            raise ValueError(f"Input '{input_option}' tidak valid untuk factor '{factor_id}'")

        return weights[input_option]

    @staticmethod
    def get_risk_rule(score: int):
        rule = (
            RiskMatrixRule.query
            .filter(RiskMatrixRule.min_score <= score)
            .order_by(RiskMatrixRule.min_score.desc())
            .first()
        )

        if not rule:
            raise ValueError(f"Tidak ada rule risiko untuk skor {score}")

        return rule

    @staticmethod
    def create_assessment(data: dict):

        prob_weight = RiskService.get_weights("probability", data["prob_input"])
        sev_weight = RiskService.get_weights("severity", data["sev_input"])
        comp_multiplier = RiskService.get_weights("competency", data["comp_input"])

        score = RiskService.calculate_score(prob_weight, sev_weight, comp_multiplier)

        rule = RiskService.get_risk_rule(score)

        assessment = RiskAssessment(
            employee_id=data["employee_id"],
            location_area=data["location_area"],
            prob_input=data["prob_input"],
            sev_input=data["sev_input"],
            comp_input=data["comp_input"],
            prob_weight=prob_weight,
            sev_weight=sev_weight,
            comp_multiplier=comp_multiplier,
            calculated_score=score,
            final_action=rule.action_suggestion,
            assessment_date=datetime.now()
        )

        db.session.add(assessment)
        db.session.commit()

        return {
            "employee_id": assessment.employee_id,
            "location_area": assessment.location_area,
            "score": score,
            "risk_level": rule.risk_level,
            "suggestion": rule.action_suggestion,
            "details": {
                "prob_weight": prob_weight,
                "sev_weight": sev_weight,
                "comp_multiplier": comp_multiplier
            }
        }
