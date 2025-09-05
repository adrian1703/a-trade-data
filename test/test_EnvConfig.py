import os
import unittest

from app.helper.EnvConfig import EnvConfig


class EnvConfigTest(EnvConfig):
    def __init__(self):
        super().__init__()
        self.test = os.getenv("test")


class TestEnvConfig(unittest.TestCase):
    def test_get_date_from_key(self):
        env_config = EnvConfigTest()
        self.assertEqual(env_config.test, "hello")


if __name__ == "__main__":
    unittest.main()
