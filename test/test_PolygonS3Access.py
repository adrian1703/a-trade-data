import unittest
from datetime import date, timedelta

from app.polygon.PolygonS3Access import PolygonS3Access


class TestPolygonS3Access(unittest.TestCase):
    def test_get_date_from_key(self):
        key = "us_stocks_sip/day_aggs_v1/2023/03/2023-03-15.csv.gz"
        self.assertEqual(PolygonS3Access._get_date_from_key(key), "2023-03-15")

    def test_full_filename_to_key(self):
        filename = "2023-07-01.csv.gz"
        kind = "minute_aggs_v1"
        key = PolygonS3Access._full_filename_to_s3key(filename, kind)
        self.assertEqual(key, "us_stocks_sip/minute_aggs_v1/2023/07/2023-07-01.csv.gz")

    def test_key_is_within_given_years_recent(self):
        # Key representing yesterday
        yesterday = date.today() - timedelta(days=1)
        key = f"us_stocks_sip/day_aggs_v1/{yesterday.year}/{yesterday.month:02d}/{yesterday.isoformat()}.csv.gz"
        self.assertTrue(PolygonS3Access._key_is_within_given_years(key, 5))

    def test_key_is_within_given_years_too_old(self):
        # Key representing 10 years ago
        d = date.today().replace(year=date.today().year - 10)
        key = f"us_stocks_sip/day_aggs_v1/{d.year}/{d.month:02d}/{d.isoformat()}.csv.gz"
        self.assertFalse(PolygonS3Access._key_is_within_given_years(key, 5))


if __name__ == "__main__":
    unittest.main()
