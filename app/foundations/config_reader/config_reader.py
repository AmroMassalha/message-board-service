from __future__ import annotations

import glob
import json
import logging
import os
from typing import Any
from typing import Dict

from foundations.admin.singleton import Singleton


class ConfigReader(metaclass=Singleton):
    def __init__(self, root_dit: str):
        self.root_dir = root_dit
        self.env = os.environ.get("ENV", "development")
        self.config = {}
        self._read_config()

    def _read_config(self):
        try:
            path = os.path.join(self.root_dir, "config", self.env, "*.json")
            logging.info(f"Looking for config files in: {path}")
            config_files = glob.glob(path)
            for file in config_files:
                with open(file) as config_file:
                    config_data = json.load(config_file)
                    if os.path.basename(file) == "database.json":
                        self._replace_db_config(config_data)
                    self.config.update(config_data)
        except Exception as e:
            logging.error(f"Error reading config files: {e}")
            raise

    def _replace_db_config(self, config_data):
        if "db_config" in config_data:
            db_config = config_data["db_config"]
            db_config["user"] = os.environ.get("MYSQL_USER", db_config.get("user"))
            db_config["password"] = os.environ.get("MYSQL_PASSWORD", db_config.get("password"))
            db_config["host"] = os.environ.get("MYSQL_HOST", db_config.get("host"))

    def get_config(self) -> Dict[str, Any]:
        return self.config
