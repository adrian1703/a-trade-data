import csv
import gzip
import logging
import os

from confluent_kafka import avro
from confluent_kafka.admin import AdminClient
from confluent_kafka.avro import AvroProducer

from app.generated.kafka_message.StockAggregate import StockAggregate
from app.helper.EnvConfig import EnvConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_list_files(path: str) -> list[str]:
    """
    Return a sorted list of full paths to all .gz files in the specified directory.
    Args:
        path (str): The directory path in which to search for .gz files.
    Returns:
        list[str]: Sorted list of full file paths for all .gz files found in the directory.
    """
    file_names = os.listdir(path)
    file_names = [f for f in file_names if f.endswith('.gz')]
    file_names.sort()
    full_file_names = [os.path.join(path, f) for f in file_names]
    return full_file_names


def _transform_csvgz_to_StockAggregate(full_file_path: str) -> list[StockAggregate]:
    """
    Reads a compressed CSV (.gz) file and transforms each row into a StockAggregate object.
    Assumes each CSV row can be used to instantiate a StockAggregate with a dict.
    Args:
        full_file_path (str): The full path to the .gz file containing CSV-formatted stock data.
    Returns:
        list[StockAggregate]: A list of StockAggregate objects parsed from each row of the CSV file.
            Returns an empty list if the file extension is not '.gz'.
    """
    if not full_file_path.endswith('.gz'):
        return []

    result = []
    with gzip.open(full_file_path, "rt", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["timestamp"] = int(row["window_start"])
            row["open"] = float(row["open"])
            row["high"] = float(row["high"])
            row["low"] = float(row["low"])
            row["close"] = float(row["close"])
            row["volume"] = int(row["volume"])
            agg = StockAggregate(row)
            result.append(agg)

    return result


class KafkaRootPublisher:
    __env_config: EnvConfig = EnvConfig()

    def __init__(self):
        schema_str = None
        with open(self.__env_config.shared_resources_dir + "StockAggregate.avsc", "r") as f:
            schema_str = f.read()
        value_schema = avro.loads(schema_str)

        self.configuration_producer: dict = {
            "bootstrap.servers": self.__env_config.kafka_broker,
            "client.id": "a-trade-data-root-publisher",
            "schema.registry.url": self.__env_config.schema_registry_url,

        }
        self.configuration_admin: dict = {
            "bootstrap.servers": self.__env_config.kafka_broker,
            "client.id": "a-trade-data-root-admin",
        }
        self.producer = AvroProducer(self.configuration_producer, default_value_schema=value_schema)
        self.admin = AdminClient(self.configuration_admin)
        self.data_dir: str = self.__env_config.data_dir

    def publish_minute_agg(self):
        self._publish(self.__env_config.minute_agg_kind, self.__env_config.minute_agg_dir)

    def publish_day_agg(self):
        self._publish(self.__env_config.day_agg_kind, self.__env_config.day_agg_dir)

    def purge_minute_agg(self):
        self._purge(self.__env_config.minute_agg_kind)

    def purge_day_agg(self):
        self._purge(self.__env_config.day_agg_kind)

    def _purge(self, topic: str):
        """
        Deletes a Kafka topic. With auto.create.topics.enable=true, the topic is recreated automatically when accessed.
        """
        fs = self.admin.delete_topics([topic])
        for t, f in fs.items():
            try:
                f.result()  # Wait for deletion to finish.
                logger.info(f"Topic '{t}' deleted.")
            except Exception as e:
                logger.info(f"Failed to delete topic '{t}': {e}")

    def _publish(self, topic: str, data_dir: str):
        files_to_publish = _get_list_files(data_dir)
        for file_path in files_to_publish:
            logger.info(f"Publishing {file_path}")
            stock_aggregates = _transform_csvgz_to_StockAggregate(file_path)
            self._publish_aggregates(topic, stock_aggregates)

    def _publish_aggregates(self, topic: str, aggs: list[StockAggregate]):
        for agg in aggs:
            self.producer.produce(topic=topic, value=agg.dict())
        self.producer.flush()
