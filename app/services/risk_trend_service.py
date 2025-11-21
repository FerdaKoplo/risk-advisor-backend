from models.risk_assesment import RiskAssessment
from datetime import datetime, timedelta
from sqlalchemy import func
from extension import db


class RiskTrendService:

    @staticmethod
    def daily_trend(days: int = 7):
        today = datetime.now()
        start_date = today - timedelta(days=days)

        results = (
            db.session.query(
                func.date(RiskAssessment.assessment_date).label("date"),
                func.avg(RiskAssessment.calculated_score).label("avg_score")
            )
            .filter(RiskAssessment.assessment_date >= start_date)
            .group_by(func.date(RiskAssessment.assessment_date))
            .order_by(func.date(RiskAssessment.assessment_date).asc())
            .all()
        )

        return [
            {
                "date": str(r.date),
                "avg_score": float(r.avg_score)
            }
            for r in results
        ]

    @staticmethod
    def monthly_trend(months: int = 6):
        today = datetime.now()
        start_date = today - timedelta(days=months * 30)

        results = (
            db.session.query(
                func.date_format(RiskAssessment.assessment_date, "%Y-%m").label("month"),
                func.avg(RiskAssessment.calculated_score).label("avg_score")
            )
            .filter(RiskAssessment.assessment_date >= start_date)
            .group_by(func.date_format(RiskAssessment.assessment_date, "%Y-%m"))
            .order_by(func.date_format(RiskAssessment.assessment_date, "%Y-%m"))
            .all()
        )

        return [
            {
                "month": r.month,
                "avg_score": float(r.avg_score)
            }
            for r in results
        ]
