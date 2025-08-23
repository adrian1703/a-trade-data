import os

from src.EnvConfig import EnvConfig


class EnvConfigTest(EnvConfig):
    def __init__(self):
        super().__init__()
        self.test: str = os.getenv("test")

    def assert_test(self):
        assert self.test == "hello"

env_config = EnvConfigTest()
print("Test: " + env_config.test)
env_config.assert_test()