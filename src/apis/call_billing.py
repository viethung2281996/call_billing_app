import logging
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from sqlalchemy import func


from src import schemas, services, models, db
from . import apis


logger = logging.getLogger('api')


class CallApi(Resource):
    schema = schemas.CallSchema()

    def put(self, user_name):
        data = request.get_json(force=True)
        data['user_name'] = user_name

        call_data = self.schema.load(data)
        user_db = services.get_or_create_user(call_data['user_name'])
        services.add_call_billing(user_db.id, call_data['call_duration'])
        logger.info(f'Add new call billing {data}')
        return {"success": True}, HTTPStatus.OK


class BillingApi(Resource):
    def get(self, user_name):
        logger.info(f'{user_name} get billing')
        user_db = db.session.query(models.User).filter(models.User.user_name == user_name).first()
        if not user_db:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        call_count = db.session.query(models.CallBilling).filter(models.CallBilling.user_id == user_db.id).count()

        block_count = db.session.query(func.sum(models.CallBilling.block_count))\
            .filter(models.CallBilling.user_id == user_db.id)\
            .group_by(models.CallBilling.user_id).first()[0]
        return {'call_count': call_count, 'block_count': block_count}, HTTPStatus.OK


apis.add_resource(CallApi, '/mobile/<string:user_name>/call')
apis.add_resource(BillingApi, '/mobile/<string:user_name>/billing')
