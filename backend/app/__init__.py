from flask import Flask
from flask_cors import CORS
from app.db import db
# Импорт моделей для регистрации
from app.models import *
from app.api import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    CORS(app)
    register_blueprints(app)
    return app 