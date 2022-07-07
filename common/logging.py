import logging
from logging.config import dictConfig
import flask

from dynaconf import settings
from flask import has_request_context, request


class RestContextFilter(logging.Filter):
    def filter(self, record):
        if not has_request_context():
            return False
        record.request_id = flask.g.get('request_id')
        record.full_path = request.full_path
        record.request_method = request.method
        try:
            record.user_id = flask.g.user_id
            if not record.user_id:
                record.user_id = -1
        except Exception:
            record.user_id = -1

        return super().filter(record)


class AppLogFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.remote_addr = request.remote_addr
            record.request_id = flask.g.get('request_id')
        else:
            record.remote_addr = None
            record.request_id = None
        return super().format(record)


def config():
    formatters = {
        'default': {
            "()": "common.logging.AppLogFormatter",
            'format': '[%(asctime)s] name=%(name)s %(levelname)s request_id=%(request_id)s remote_addr=%(remote_addr)s '
                      'message=%(message)s'
        },
        'rest_api': {
            "()": "common.logging.AppLogFormatter",
            'format': '[%(asctime)s] name=%(name)s %(levelname)s REST_API user_id=%(user_id)d '
                      'method=%(request_method)s full_path=%(full_path)-8s request_id=%(request_id)s '
                      'remote_addr=%(remote_addr)s message=%(message)s'
        }
    }
    handlers = {
        'rest_api': {
            'class': 'logging.StreamHandler',
            'formatter': 'rest_api',
            'filters': ['jwt_filter'],
        },
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    }
    filters = {
        'jwt_filter': {
            '()': RestContextFilter
        }
    }
    loggers = {
        'api': {
            'handlers': ['rest_api'],
            'propagate': False,
        },
        'default': {
            'handlers': ['default'],
            'propagate': False,
        },
    }
    dictConfig({
        'version': 1,
        'formatters': formatters,
        'filters': filters,
        'handlers': handlers,
        'loggers': loggers
    })
    log_level = logging.getLevelName(settings.get('LOG_LEVEL', logging.INFO))
    logging.basicConfig(level=log_level)
    logging.getLogger('src').setLevel(log_level)
    logging.getLogger('parso').setLevel(logging.ERROR)
