from flask import Flask

from app.beackend.config import BaseConfig
from app.beackend.database.connection import Connection
from app.beackend.routes.login import register


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(register)

    with app.app_context():
        Connection(BaseConfig().get_connection())

    return app
