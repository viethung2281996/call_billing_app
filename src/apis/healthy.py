from http import HTTPStatus
from flask_restful import Resource

from . import apis


class Healthy(Resource):
    def get(self):
        return {'status': True}, HTTPStatus.OK


apis.add_resource(Healthy, '/healthy')
