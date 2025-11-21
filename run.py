from app import create_app, db
from app.utils.config import Config


from app.models import (
    RiskAssessment,
    RiskFactorDefinition,
    RiskMatrixRule
)

app = create_app(Config) 

if __name__ == '__main__':
    print(f"Menjalankan Flask App dengan konfigurasi: {Config.SQLALCHEMY_DATABASE_URI}")
    app.run(debug=True, port=5000)