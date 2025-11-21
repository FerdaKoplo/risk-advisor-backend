from models.risk_matrix_rule import RiskMatrixRule
from extension import db


class RiskRuleService:

    @staticmethod
    def get_rule_by_score(score: int):
        rule = (
            RiskMatrixRule.query
            .filter(RiskMatrixRule.min_score <= score)
            .order_by(RiskMatrixRule.min_score.desc())
            .first()
        )
        return rule

    @staticmethod
    def get_all_rules():
        return [
            r.to_dict()
            for r in RiskMatrixRule.query.order_by(RiskMatrixRule.min_score.asc()).all()
        ]

    @staticmethod
    def seed_default_rules():

        default = [
            { "min_score": 0, "risk_level": "Low", "action_suggestion": "Tetap bekerja dengan aman." },
            { "min_score": 30, "risk_level": "Medium", "action_suggestion": "Lakukan pengecekan APD dan prosedur safety." },
            { "min_score": 60, "risk_level": "High", "action_suggestion": "Hentikan aktivitas. Analisis bahaya sebelum melanjutkan." },
            { "min_score": 90, "risk_level": "Extreme", "action_suggestion": "Segera lakukan tindakan mitigasi darurat." }
        ]

        for item in default:
            exists = RiskMatrixRule.query.filter_by(min_score=item["min_score"]).first()
            if not exists:
                db.session.add(RiskMatrixRule(**item))

        db.session.commit()
