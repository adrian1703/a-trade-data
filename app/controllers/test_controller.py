import logging

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from app.publisher.KafkaRootPublisher import KafkaRootPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def v1_test_publish():  # noqa: E501
    """
    Publishes a sample message to a Kafka topic using an Avro schema.
    Enhanced with comprehensive logging at each step.
    :return: A confirmation string indicating successful data publication.
    :rtype: str
    """
    logger.info("Purging aggregate data: starting process")
    try:
        logger.debug("Initializing KafkaRootPublisher...")
        publisher = KafkaRootPublisher()
        value_schema_str = """
        {
          "type": "record",
          "name": "User",
          "namespace": "example.avro",
          "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "int"},
            {"name": "email", "type": "string"}
          ]
        }
        """
        logger.info("Parsing Avro schema...")
        value_schema = avro.loads(value_schema_str)
        logger.debug("Avro schema loaded successfully.")

        logger.info("Initializing AvroProducer with configuration: %s", publisher.configuration_producer)
        producer = AvroProducer(publisher.configuration_producer, default_value_schema=value_schema)

        topic = "users-avro"
        value = {"name": "Alice", "age": 30, "email": "alice@example.com"}
        logger.info(f"Producing message to topic '{topic}' with value: {value}")

        producer.produce(topic=topic, value=value)
        logger.info("Message produced, waiting for flush/acknowledgement...")

        producer.flush()
        logger.info("Message successfully delivered to Kafka topic '%s'.", topic)

        return 'Data published!'

    except Exception as ex:
        logger.error("Exception occurred during Kafka publish: %s", ex, exc_info=True)
        raise
