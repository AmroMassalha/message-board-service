from __future__ import annotations

import logging

import pika
from pika.exceptions import AMQPConnectionError


class RabbitMQManager:
    def __init__(self, mq_config: dict):
        self.mq_config = mq_config
        self._setup_logging()
        _credentials = pika.PlainCredentials(self.mq_config["user"], self.mq_config["password"])
        parameters = pika.ConnectionParameters(self.mq_config["host"], self.mq_config["port"], "/", _credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.queue_name = self.mq_config["queue_name"]

    def _setup_logging(self):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def create_queue(self):
        try:
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            logging.info(f"Queue '{self.queue_name}' is declared successfully.")
        except AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ server: {e}")
        except Exception as e:
            logging.error(f"Failed to declare queue: {e}")
