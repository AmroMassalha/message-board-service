from __future__ import annotations

import logging
from abc import ABC

from foundations.config_reader.config_reader import ConfigReader


class AbstractApiGateway(ABC):
    def __init__(self, root_dir: str):
        self.config_reader = ConfigReader(root_dir)
        self.config = None
        try:
            self.config = self.config_reader.get_config()
        except Exception as e:
            logging.error(f"Error while reading config: {e}")
            raise

        if self.config:
            for service, url in self.config.items():
                setattr(self, service, url)
