from extension import db
from datetime import datetime
from typing import Dict, Any, List

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.String(50), nullable=False, index=True)
    location_area = db.Column(db.String(100), nullable=False)

    prob_input = db.Column(db.String(50))
    sev_input = db.Column(db.String(50))
    comp_input = db.Column(db.String(50))

    prob_weight = db.Column(db.Integer, nullable=False)
    sev_weight = db.Column(db.Integer, nullable=False)
    comp_multiplier = db.Column(db.Float, nullable=False)

    calculated_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)

    final_action = db.Column(db.Text, nullable=False)

    metadata = db.Column(db.JSON, nullable=True)

    assessment_date = db.Column(db.DateTime, default=datetime.now, index=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "location_area": self.location_area,
            "prob_input": self.prob_input,
            "sev_input": self.sev_input,
            "comp_input": self.comp_input,
            "prob_weight": self.prob_weight,
            "sev_weight": self.sev_weight,
            "comp_multiplier": self.comp_multiplier,
            "calculated_score": self.calculated_score,
            "final_action": self.final_action,
            "assessment_date": self.assessment_date.isoformat()
        }