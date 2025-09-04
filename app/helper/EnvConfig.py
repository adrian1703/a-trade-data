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
        self.shared_resources_dir: str = os.getenv("shared_resources_dir")
        self.kafka_broker: str = os.getenv("kafka_broker")
        self.schema_registry_url: str = os.getenv("schema_registry_url")

        if not self.data_dir.endswith('/'):
            self.data_dir += '/'
        if not self.shared_resources_dir.endswith('/'):
            self.shared_resources_dir += '/'

        self.day_agg_kind = "day_aggs_v1"
        self.minute_agg_kind = "minute_aggs_v1"
        self.day_agg_dir: str = self.data_dir + self.day_agg_kind + '/'
        self.minute_agg_dir: str = self.data_dir + self.minute_agg_kind + '/'
        assert self.aws_access_key_id is not None
        assert self.aws_secret_access_key is not None
        assert self.data_dir is not None
        assert self.shared_resources_dir is not None
