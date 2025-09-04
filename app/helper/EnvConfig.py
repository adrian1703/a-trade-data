import os

from dotenv import load_dotenv, find_dotenv


class EnvConfig:

    @staticmethod
    def __load_env():
        load_dotenv(find_dotenv(".env"))

    def __init__(self):
        self.__load_env()
        self.aws_access_key_id: str = os.getenv("aws_access_key_id")
        self.aws_secret_access_key: str = os.getenv("aws_secret_access_key")
        self.data_dir: str = os.getenv("data_dir")
        assert self.aws_access_key_id is not None
        assert self.aws_secret_access_key is not None
        assert self.data_dir is not None