import os

from dotenv import load_dotenv, find_dotenv


class EnvConfig:

    @staticmethod
    def __load_env():
        load_dotenv(find_dotenv())

    def __init__(self):
        self.__load_env()
        self.aws_access_key_id: str = os.getenv("aws_access_key_id")
        self.aws_secret_access_key: str = os.getenv("aws_secret_access_key")