import logging
import os
from unittest import TestCase

from src import create_app, db
from faker import Faker
from flask_jwt_extended import create_access_token
from sqlalchemy.orm.session import close_all_sessions

logger = logging.getLogger('default')


class BaseTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        logger.info('Setup test client')
        super().setUp(*args, **kwargs)
        env_var = os.getenv('FLASK_ENV')
        if env_var:
            self.app = create_app(env_var)
        else:
            self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.faker = Faker()

        try:
            db.drop_all()
        except Exception:
            pass

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self, *args, **kwargs):
        logger.info('Teardown test client')
        super().tearDown(*args, **kwargs)
        logger.debug('Drop database')
        close_all_sessions()
        db.drop_all()
        logger.debug('Pop app context')
        self.app_context.pop()

    def _create_access_token(self, user_id, user_name, roles):
        user_claims = {
            'name': user_name,
            'roles': roles
        }
        return create_access_token(identity=user_id, additional_claims=user_claims)

    def _generate_api_header(self, access_token=None, **kwargs):
        base = {
            **kwargs,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if access_token:
            base['Authorization'] = f'Bearer {access_token}'
        return base
