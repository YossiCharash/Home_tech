from flask import Flask
from flask_cors import CORS

from beackend.config import BaseConfig
from beackend.database.connection import Connection
from beackend.routes.login.login import register


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(register)

    with app.app_context():
        Connection(BaseConfig().get_connection())
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

    return app
