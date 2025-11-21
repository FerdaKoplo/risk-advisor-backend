import random
from datetime import datetime, timedelta
from app import create_app
from app.extension import db
from app.models.risk_matrix_rule import RiskMatrixRule
from app.models.risk_factor_definitions import RiskFactorDefinition
from app.models.risk_assesment import RiskAssessment

app = create_app()

def seed_risk_matrix_rules():
    rules = [
        {"min_score": 0, "max_score": 3, "risk_level": "LOW"},
        {"min_score": 4, "max_score": 6, "risk_level": "MEDIUM"},
        {"min_score": 7, "max_score": 9, "risk_level": "HIGH"},
        {"min_score": 10, "max_score": 15, "risk_level": "CRITICAL"}
    ]
    for r in rules:
        rule = RiskMatrixRule(
            min_score=r["min_score"],
            max_score=r["max_score"],
            risk_level=r["risk_level"]
        )
        db.session.add(rule)
    db.session.commit()
    print("Seeded RiskMatrixRule")

def seed_risk_factor_definitions():
    factors = [
        {"factor_id": "probability", "label": "Probability", "weights": {"low": 1, "medium": 2, "high": 3}},
        {"factor_id": "severity", "label": "Severity", "weights": {"low": 1, "medium": 2, "high": 3}},
        {"factor_id": "competency", "label": "Competency", "weights": {"low": 0.5, "medium": 1, "high": 1.5}},
    ]
    for f in factors:
        factor = RiskFactorDefinition(factor_id=f["factor_id"], label=f["label"])
        factor.weights = f["weights"]
        db.session.add(factor)
    db.session.commit()
    print("Seeded RiskFactorDefinition")

def seed_risk_assessments(n=20):
    locations = ["Warehouse A", "Warehouse B", "Office HQ", "Factory Floor", "Site C"]
    employees = [f"E{str(i).zfill(3)}" for i in range(1, 21)]
    rules = RiskMatrixRule.query.all()

    for _ in range(n):
        employee_id = random.choice(employees)
        location = random.choice(locations)
        prob_input = random.choice(["low", "medium", "high"])
        sev_input = random.choice(["low", "medium", "high"])
        comp_input = random.choice(["low", "medium", "high"])

        prob_weight = RiskFactorDefinition.query.filter_by(factor_id="probability").first().weights[prob_input]
        sev_weight = RiskFactorDefinition.query.filter_by(factor_id="severity").first().weights[sev_input]
        comp_multiplier = RiskFactorDefinition.query.filter_by(factor_id="competency").first().weights[comp_input]

        calculated_score = round((prob_weight + sev_weight) * comp_multiplier, 2)

        matched_rule = next((r for r in rules if r.min_score <= calculated_score <= r.max_score), None)
        risk_level = matched_rule.risk_level if matched_rule else "UNKNOWN"

        assessment = RiskAssessment(
            employee_id=employee_id,
            location_area=location,
            prob_input=prob_input,
            sev_input=sev_input,
            comp_input=comp_input,
            prob_weight=prob_weight,
            sev_weight=sev_weight,
            comp_multiplier=comp_multiplier,
            calculated_score=calculated_score,
            risk_level=risk_level,
            assessment_date=datetime.now() - timedelta(days=random.randint(0, 365))
        )
        db.session.add(assessment)

    db.session.commit()
    print(f"Seeded {n} RiskAssessment records")

if __name__ == "__main__":
    with app.app_context():
        RiskAssessment.query.delete()
        RiskMatrixRule.query.delete()
        RiskFactorDefinition.query.delete()
        db.session.commit()

        seed_risk_matrix_rules()
        seed_risk_factor_definitions()
        seed_risk_assessments(n=1000)
