from app.extension import db
from typing import Dict, Any
import json


class RiskFactorDefinition(db.Model):
    __tablename__ = 'risk_factor_definitions'
    
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    
    factor_id = db.Column(db.String(50), unique=True, nullable=False) 
    label = db.Column(db.String(100), nullable=False)
    
    _weights_json = db.Column('weights', db.Text, nullable=False)

    @property
    def weights(self) -> Dict[str, float]:
        return json.loads(self._weights_json)

    @weights.setter
    def weights(self, value: Dict[str, float]):
        self._weights_json = json.dumps(value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_id": self.factor_id,
            "label": self.label,
            "weights": self.weights
        }