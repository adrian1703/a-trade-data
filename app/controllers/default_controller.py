import logging

from app.polygon.PolygonS3Access import PolygonS3Access
from app.publisher.KafkaRootPublisher import KafkaRootPublisher
from openapi_server.models import FetchAggregateDataResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

polygon_s3_access = PolygonS3Access()
kafka_root_publisher = KafkaRootPublisher()


def v1_fetch_aggregate_data_post():  # noqa: E501
    """Fetches minute and daily aggregates dating back 5 years

     # noqa: E501

    :rtype: Union[FetchAggregateDataResult, Tuple[FetchAggregateDataResult, int], Tuple[FetchAggregateDataResult, int, Dict[str, str]]
    """
    logger.info("Fetching aggregate data: starting process")

    pages_fetched = polygon_s3_access.fetch_pages()
    logger.info("Pages fetched: %d", pages_fetched)

    day_agg_downloaded = polygon_s3_access.download_missing_day_agg()
    logger.info("Day aggregates downloaded: %d", day_agg_downloaded)

    min_agg_downloaded = polygon_s3_access.download_missing_minute_agg()
    logger.info("Minute aggregates downloaded: %d", min_agg_downloaded)

    logger.info("Fetching aggregate data: finished process")
    return FetchAggregateDataResult(
        pages_fetched=pages_fetched,
        day_agg_downloaded=day_agg_downloaded,
        min_agg_downloaded=min_agg_downloaded
    )


def v1_publish_aggregate_data_post():  # noqa: E501
    """Publish aggregate data to Kafka

     # noqa: E501

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    logger.info("Publish aggregate data called")
    kafka_root_publisher.publish_day_agg()
    kafka_root_publisher.publish_minute_agg()
    return 'Data published!'


def v1_purge_aggregate_data_post():  # noqa: E501
    """Purge published data to Kafka

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    logger.info("Purging aggregate data: starting process")
    kafka_root_publisher.purge_day_agg()
    kafka_root_publisher.purge_minute_agg()
    logger.info("Purging aggregate data: finished process")
    return 'Data purged!'
