import os
import pytest

from helper.EnvConfig import EnvConfig


class EnvConfigTest(EnvConfig):
    def __init__(self):
        super().__init__()
        self.test: str = os.getenv("test")

    def assert_test(self):
        assert self.test == "hello"

def test_get_date_from_key():
    env_config = EnvConfigTest()
    assert env_config.test == "hello"