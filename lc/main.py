"""Main module"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

import logging
import logging.config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    logging.config.dictConfig(app.config.get("LOGGING"))

    from lc.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')
    return app
