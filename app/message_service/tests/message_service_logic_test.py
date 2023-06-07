from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from message_service.logic.concrete_message_service import ConcreteMessageService


class TestConcreteMessageService(unittest.TestCase):
    @patch(
        "foundations.config_reader.config_reader.ConfigReader",
        return_value={
            "APP_SECRET_KEY": "secret_key",
            "db_config": {
                "user": "myuser",
                "password": "mypassword",
                "host": "database",
                "database": "message_board",
                "table": "messages",
                "port": 3306,
                "auth_plugin": "mysql_native_password",
                "charset": "utf8mb4",
                "use_pure": True,
            },
        },
    )
    @patch("foundations.database.database_client.DatabaseClient")
    @patch("foundations.database.query_builder.QueryBuilder")
    def setUp(self, mock_query_builder, mock_db_client, mock_config_reader):
        self.mock_db_client = MagicMock()
        mock_db_client.return_value = self.mock_db_client

        self.mock_query_builder = MagicMock()
        mock_query_builder.return_value = self.mock_query_builder

        self.mock_config_reader = MagicMock()
        mock_config_reader.return_value = self.mock_config_reader

        self.message_service = ConcreteMessageService("root_directory")

    @patch.object(ConcreteMessageService, "query_builder")
    @patch.object(ConcreteMessageService, "db_client")
    def test_create_message(self, mock_db_client, mock_query_builder):
        mock_query_builder.insert.return_value = "mock_query"
        mock_db_client.execute_query.return_value = None
        mock_db_client.get_last_insert_id.return_value = 1

        result = self.message_service.create_message("user_id", "message")

        self.assertEqual(result, "1")

    @patch.object(ConcreteMessageService, "query_builder")
    @patch.object(ConcreteMessageService, "db_client")
    def test_view_messages(self, mock_db_client, mock_query_builder):
        mock_query_builder.select_all.return_value = "mock_query"
        mock_db_client.execute_query.return_value = [("message1",), ("message2",)]

        result = self.message_service.view_messages()

        self.assertEqual(result, [("message1",), ("message2",)])

    @patch("requests.post")
    def test_vote_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"vote_count": 10}
        mock_post.return_value = mock_response

        result = self.message_service.vote_message("user_id", "message_id", "vote_type")

        self.assertEqual(result, 10)

    @patch.object(ConcreteMessageService, "query_builder")
    @patch.object(ConcreteMessageService, "db_client")
    def test_delete_message(self, mock_db_client, mock_query_builder):
        mock_query_builder.delete.return_value = "mock_query"
        mock_db_client.execute_query.return_value = None

        # No assertion needed if not expecting a result
        self.message_service.delete_message("user_id", "message_id")

    @patch.object(ConcreteMessageService, "query_builder")
    @patch.object(ConcreteMessageService, "db_client")
    def test_view_user_messages(self, mock_db_client, mock_query_builder):
        mock_query_builder.select_where.return_value = "mock_query"
        mock_db_client.execute_query.return_value = [("message1",), ("message2",)]

        result = self.message_service.view_user_messages("user_id")

        self.assertEqual(result, [("message1",), ("message2",)])


if __name__ == "__main__":
    unittest.main()
