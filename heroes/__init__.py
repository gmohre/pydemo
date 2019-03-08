import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import configs


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configs[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    db.init_app(app)
    with app.app_context():
        from . import api, heroes
        app.register_blueprint(api.bp)
        app.register_blueprint(heroes.bp)
        db.create_all()
        return app