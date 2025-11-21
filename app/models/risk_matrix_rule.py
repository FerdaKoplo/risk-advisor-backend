from app.extension import db
from typing import Dict, Any


class RiskMatrixRule(db.Model):
    __tablename__ = 'risk_matrix_rules'
    __table_args__ = (
        db.Index('range_idx', 'min_score', 'max_score'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    id = db.Column(db.Integer, primary_key=True)
    min_score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)

    risk_level = db.Column(db.String(50), nullable=False)
    action_suggestion = db.Column(db.Text, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "min_score": self.min_score,
            "risk_level": self.risk_level,
            "action_suggestion": self.action_suggestion
        }