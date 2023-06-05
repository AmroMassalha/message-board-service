import unittest
from unittest.mock import patch, MagicMock
from flask import json

from user_service.app import UserServiceApplication

class TestUserService(unittest.TestCase):

    @patch('foundations/database/database_client.DatabaseClient')
    def setUp(self):
        self.app = UserServiceApplication().app
        self.app.testing = True
        self.test_client = self.app.test_client()

    @patch('user_service.app.ConcreteUserServiceLogic')
    def test_get_all_users(self, MockLogic):
        with self.app.app_context():
            mock_get_all_user = MockLogic.return_value.get_all_user
            mock_get_all_user.return_value = [('user1', 'password1'), ('user2', 'password2')]

            response = self.test_client.get("/users")
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [('user1', 'password1'), ('user2', 'password2')])

    @patch('user_service.app.ConcreteUserServiceLogic')
    def test_get_user(self, MockLogic):
        with self.app.app_context():
            mock_get_user = MockLogic.return_value.get_user
            mock_get_user.return_value = [('user1', 'password1')]

            response = self.test_client.get("/users/1")
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [('user1', 'password1')])

    @patch('user_service.app.ConcreteUserServiceLogic')
    def test_create_user(self, MockLogic):
        with self.app.app_context():
            mock_create_user = MockLogic.return_value.create_user
            mock_create_user.return_value = "User created successfully"

            response = self.test_client.post("/register", json={'username': 'user1', 'password': 'password1'})

            self.assertEqual(response.status_code, 201)
            self.assertEqual(json.loads(response.data)["msg"], "User created successfully")


if __name__ == '__main__':
    unittest.main()
