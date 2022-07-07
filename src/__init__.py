from flask import Flask
import logging
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from dynaconf import settings
from marshmallow.exceptions import MarshmallowError
from werkzeug.exceptions import NotFound

from common.api import add_request_id
from common.logging import config as config_logging
from common import error_handling

logger = logging.getLogger(__name__)

db = SQLAlchemy(metadata=declarative_base().metadata,
                engine_options={'connect_args': {
                    'connect_timeout': 10
                }})


def create_app(flask_env, db_uri=None):
    config_logging()
    app = Flask(__name__)
    logger.info('Loading configuration')
    load_configuration(app, flask_env)
    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    logger.info('Initializing app')
    db.init_app(app)

    from .apis import api_bp
    logger.info('Registering blueprints')
    app.register_blueprint(api_bp, url_prefix='/api')

    app.register_error_handler(MarshmallowError, error_handling.handle_validation_error)
    app.register_error_handler(NotFound, error_handling.handle_not_found)
    app.register_error_handler(Exception, error_handling.handle_unknow_exception)

    app.before_request(add_request_id)
    return app


def load_configuration(app, flask_env):
    if flask_env is None:
        raise Exception('Missing config FLASK_ENV in environment valiables')
    settings.setenv(flask_env.upper())
    config_dict = settings.as_dict(env=flask_env)
    for key, val in config_dict.items():
        app.config[key] = val
