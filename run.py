from app import create_app, db
from app.utils.config import Config
from app.services.risk_service import RiskService

from app.models import (
    RiskAssessment,
    RiskFactorDefinition,
    RiskMatrixRule
)

app = create_app(Config) 

with app.app_context():
    RiskService.load_ml_model()

if __name__ == '__main__':
    print(f"Menjalankan Flask App dengan konfigurasi: {Config.SQLALCHEMY_DATABASE_URI}")
    app.run(debug=True, port=5000)