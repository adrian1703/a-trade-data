import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server import util


def v1_fetch_aggregate_data_post():  # noqa: E501
    """Fetches minute and daily aggregates dating back 5 years

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do my magic!'


def v1_publish_aggregate_data_post():  # noqa: E501
    """Publish aggregate data to Kafka

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do my magic!'
