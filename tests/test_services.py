from src import db, models, services
from . import BaseTestCase


class TestCallService(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_db = models.User(user_name='test_user')
        db.session.add(self.user_db)
        db.session.commit()

    def test_caculate_call_block_count(self):
        call_db = services.add_call_billing(self.user_db.id, 3000)
        self.assertEqual(call_db.block_count, 1)

        call_db = services.add_call_billing(self.user_db.id, 500000)
        self.assertEqual(call_db.block_count, 17)
