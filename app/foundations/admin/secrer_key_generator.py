from foundations.admin.singleton import Singleton

import os

class SecretKeyGenerator(metaclass=Singleton):
    _secret_key = None

    def generate_key(self):
        if self._secret_key is None:
            self._secret_key = os.urandom(24).hex()
        return self._secret_key
