from http import HTTPStatus

from src import db, models, services
from . import BaseTestCase


class TestApisCall(BaseTestCase):
    def test_create_new_call_billing_for_user(self):
        payload = {"call_duration": 3000}
        user_name = 'test_user'
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)

        self.assertEqual(res.status_code, HTTPStatus.OK)

        user_db = db.session.query(models.User).filter(models.User.user_name == user_name).first()
        self.assertIsNotNone(user_db)
        call_billing_db = db.session.query(models.CallBilling).filter(models.CallBilling.user_id == user_db.id).first()
        self.assertIsNotNone(call_billing_db)
        self.assertEqual(call_billing_db.call_duration, 3000)

    def test_create_new_call_with_user_name_invalid(self):
        payload = {"call_duration": 3000}
        user_name = 'a' * 100
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        data = res.get_json()
        self.assertEqual(data['error_message'], [{'user_name': ['Length must be between 1 and 32.']}])

        payload = {"call_duration": 3000}
        res = self.client.put('/api/mobile//call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)

    def test_create_new_call_with_call_duration_invalid(self):
        payload = {"call_duration": -1000}
        user_name = 'test_user'
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        data = res.get_json()
        self.assertEqual(data['error_message'], [{'call_duration': ['Value must be greater than 0']}])

        payload = {"call_duration": None}
        user_name = 'test_user'
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        data = res.get_json()
        self.assertEqual(data['error_message'], [{'call_duration': ['Field may not be null.']}])

        payload = {"call_duration": '3000'}
        user_name = 'test_user'
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        data = res.get_json()
        self.assertEqual(data['error_message'], [{'call_duration': ['Not a valid integer.']}])

        payload = {}
        user_name = 'test_user'
        res = self.client.put(f'/api/mobile/{user_name}/call', json=payload)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        data = res.get_json()
        self.assertEqual(data['error_message'], [{'call_duration': ['Missing data for required field.']}])


class TestApisBilling(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_db_1 = models.User(user_name='test_user_1')
        db.session.add(self.user_db_1)
        db.session.commit()

        self.user_db_2 = models.User(user_name='test_user_2')
        db.session.add(self.user_db_2)
        db.session.commit()

    def test_get_api_billing(self):
        services.add_call_billing(self.user_db_1.id, 3000)
        services.add_call_billing(self.user_db_1.id, 50000)
        services.add_call_billing(self.user_db_1.id, 100000)

        services.add_call_billing(self.user_db_2.id, 120000)
        services.add_call_billing(self.user_db_2.id, 150000)
        services.add_call_billing(self.user_db_2.id, 180000)

        res = self.client.get(f'/api/mobile/{self.user_db_1.user_name}/billing')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.get_json()
        self.assertEqual(data['call_count'], 3)
        self.assertEqual(data['block_count'], 7)

        res = self.client.get(f'/api/mobile/{self.user_db_2.user_name}/billing')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.get_json()
        self.assertEqual(data['call_count'], 3)
        self.assertEqual(data['block_count'], 15)

    def test_get_api_billing_user_not_found(self):
        res = self.client.get('/api/mobile/user_not_exist/billing')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        data = res.get_json()
        self.assertEqual(data['message'], 'User not found')
