import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from app.models.risk_assesment import RiskAssessment
from app.models.risk_factor_definitions import RiskFactorDefinition
from app.models.risk_matrix_rule import RiskMatrixRule
from app.extension import db

MODEL_PATH = "risk_model.pkl"

class RiskService:
    ml_model = None

  
    @staticmethod
    def load_ml_model():
        if os.path.exists(MODEL_PATH):
            RiskService.ml_model = joblib.load(MODEL_PATH)
        else:
            RiskService.train_ml_model()

    @staticmethod
    def train_ml_model():
        assessments = RiskAssessment.query.all()
        if not assessments:
            print("No data found, cannot train ML model yet")
            return None

        df = pd.DataFrame([a.to_dict() for a in assessments])
        df = df.dropna(subset=['risk_level'])
        if df.empty:
            print("No valid labeled data for training")
            return None

        X = df[['prob_weight', 'sev_weight', 'comp_multiplier']]
        y = df['risk_level'].astype(str)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)
        RiskService.ml_model = model
        print(f"Model trained and saved to {MODEL_PATH}")
        return model

   
    @staticmethod
    def predict_risk_level(prob_weight, sev_weight, comp_multiplier):
        if RiskService.ml_model is None:
            RiskService.load_ml_model()
        if RiskService.ml_model is None:
            # fallback if no model exists
            print("ML model not available, using rule-based fallback")
            score = prob_weight * sev_weight * comp_multiplier
            rule = RiskService.get_risk_rule(score)
            return rule.risk_level
        return RiskService.ml_model.predict([[prob_weight, sev_weight, comp_multiplier]])[0]

 
    @staticmethod
    def get_weights(factor_id: str, input_option: str) -> float:
        factor = RiskFactorDefinition.query.filter_by(factor_id=factor_id).first()
        if not factor:
            raise ValueError(f"Risk factor '{factor_id}' not found")
        weights = factor.weights
        if input_option not in weights:
            raise ValueError(f"Input '{input_option}' invalid for factor '{factor_id}'")
        return weights[input_option]

    @staticmethod
    def calculate_score(prob_weight: int, sev_weight: int, comp_multiplier: float) -> int:
        return int((prob_weight * sev_weight) * comp_multiplier)

    @staticmethod
    def get_risk_rule(score: int):
        rule = RiskMatrixRule.query.filter(
            RiskMatrixRule.min_score <= score,
            RiskMatrixRule.max_score >= score
        ).first()
        if not rule:
            raise ValueError(f"No risk rule found for score {score}")
        return rule

    @staticmethod
    def create_assessment(data: dict, use_ml=True):
        prob_weight = RiskService.get_weights("probability", data["prob_input"])
        sev_weight = RiskService.get_weights("severity", data["sev_input"])
        comp_multiplier = RiskService.get_weights("competency", data["comp_input"])

        score = RiskService.calculate_score(prob_weight, sev_weight, comp_multiplier)

        if use_ml:
            risk_level = RiskService.predict_risk_level(prob_weight, sev_weight, comp_multiplier)
            final_action = "Check AI prediction"
        else:
            rule = RiskService.get_risk_rule(score)
            risk_level = rule.risk_level
            final_action = rule.action_suggestion

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
            risk_level=risk_level,
            final_action=final_action,
            assessment_date=datetime.now()
        )

        db.session.add(assessment)
        db.session.commit()

        return {
            "employee_id": assessment.employee_id,
            "location_area": assessment.location_area,
            "score": score,
            "risk_level": risk_level,
            "suggestion": final_action,
            "details": {
                "prob_weight": prob_weight,
                "sev_weight": sev_weight,
                "comp_multiplier": comp_multiplier
            }
        }
