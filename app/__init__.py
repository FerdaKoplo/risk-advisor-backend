from flask import Flask
from flask_migrate import Migrate
from app.utils.config import Config
from app.extension import db
from app.controller import api  

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api, url_prefix="/api")

    return app
