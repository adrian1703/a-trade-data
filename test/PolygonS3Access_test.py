import pytest
from datetime import date, timedelta
from src.PolygonS3Access import PolygonS3Access

def test_get_date_from_key():
    key = "us_stocks_sip/day_aggs_v1/2023/03/2023-03-15.csv.gz"
    assert PolygonS3Access.get_date_from_key(key) == "2023-03-15"

def test_full_filename_to_key():
    filename = "2023-07-01.csv.gz"
    kind = "minute_aggs_v1"
    key = PolygonS3Access._full_filename_to_key(filename, kind)
    assert key == "us_stocks_sip/minute_aggs_v1/2023/07/2023-07-01.csv.gz"

def test_key_is_within_given_years_recent():
    # Key representing yesterday
    yesterday = date.today() - timedelta(days=1)
    key = f"us_stocks_sip/day_aggs_v1/{yesterday.year}/{yesterday.month:02d}/{yesterday.isoformat()}.csv.gz"
    assert PolygonS3Access.key_is_within_given_years(key, 5)

def test_key_is_within_given_years_too_old():
    # Key representing 10 years ago
    d = date.today().replace(year=date.today().year - 10)
    key = f"us_stocks_sip/day_aggs_v1/{d.year}/{d.month:02d}/{d.isoformat()}.csv.gz"
    assert not PolygonS3Access.key_is_within_given_years(key, 5)
