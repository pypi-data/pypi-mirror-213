from flask import Flask
from flask_useful import register_blueprints


def create_app():
    app = Flask(__name__)
    register_blueprints(app, 'routes', include_packages=True)
    return app
