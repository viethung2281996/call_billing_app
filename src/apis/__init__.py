from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint('api', __name__)
apis = Api(api_bp)


from . import healthy, call_billing # noqa
