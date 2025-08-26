import os
import pickle
import boto3
from datetime import date, datetime, timedelta

from botocore.config import Config

from src.EnvConfig import EnvConfig


class PolygonS3Access:
    __env_config: EnvConfig = EnvConfig()
    _day_agg_kind = "day_aggs_v1"
    _minute_agg_kind = "minute_aggs_v1"

    def __init__(self, data_dir: str = './../data/'):
        self.__session = boto3.Session(
            aws_access_key_id=self.__env_config.aws_access_key_id,
            aws_secret_access_key=self.__env_config.aws_secret_access_key,
        )
        self.__s3 = self.__session.client(
            's3',
            endpoint_url='https://files.polygon.io',
            config=Config(signature_version='s3v4'),
        )
        self.s3pages = []
        self.years_filter = 5
        self.data_dir = self.__env_config.data_dir
        self._day_agg_dir = self.data_dir + self._day_agg_kind + '/'
        self._minute_agg_dir = self.data_dir + self._minute_agg_kind + '/'
        for dir_to_create in [self.data_dir, self._day_agg_dir, self._minute_agg_dir]:
            os.makedirs(dir_to_create, exist_ok=True)

    def save_data(self):
        with open(self.data_dir + 'cache/s3pages.pkl', 'wb') as f:
            pickle.dump(self.s3pages, f)

    def load_data(self):
        with open(self.data_dir + 'cache/s3pages.pkl', 'rb') as f:
            self.s3pages = pickle.load(f)
    
    def fetch_pages(self, prefix: str = 'us_stocks_sip'):
        paginator = self.__s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket='flatfiles', Prefix=prefix):
            self.s3pages.append(page)

    def print_pages(self):
        for page in self.s3pages:
            for obj in page['Contents']:
                print(obj['Key'])

    def download_missing_day_agg(self, dry_run: bool = False):
        self._download_missing_agg(self.get_day_agg_keys,
                                   self._day_agg_kind,
                                   self._day_agg_dir,
                                   dry_run)

    def download_missing_minute_agg(self, dry_run: bool = False):
        self._download_missing_agg(self.get_minute_agg_keys,
                                   self._minute_agg_kind,
                                   self._minute_agg_dir,
                                   dry_run)

    def download(self, object_key: str, directory: str = './'):
        if directory[-1] != '/':
            directory += '/'
        local_file_name = object_key.split('/')[-1]
        local_file_path = directory + local_file_name
        self._download(object_key, local_file_path)

    def get_day_agg_keys(self):
        return self._get_keys_of_kind(self._day_agg_kind)

    def get_minute_agg_keys(self):
        return self._get_keys_of_kind(self._minute_agg_kind)


    @staticmethod
    def get_date_from_key(key):
        return key.split("/")[4].split(".")[0]


    @staticmethod
    def key_is_within_given_years(key_to_check, years):
        date_to_check = PolygonS3Access.get_date_from_key(key_to_check)
        today = date.today() - timedelta(days=1)
        # Compute the threshold date
        try:
            threshold = today.replace(year=today.year - years)
        except ValueError:
            # Handle leap year (e.g. Feb 29)
            threshold = today.replace(month=2, day=28, year=today.year - years)
        check_date = datetime.strptime(date_to_check, "%Y-%m-%d").date()
        return check_date >= threshold

    @staticmethod
    def _full_filename_to_key(filename: str, kind: str):
        filename = filename.split("/")[-1]
        year = filename.split("-")[0]
        month = filename.split("-")[1]
        return f'us_stocks_sip/{kind}/{year}/{month}/{filename}'

    def _get_all_keys(self):
        all_keys = []
        for page in self.s3pages:
            for obj in page['Contents']:
                all_keys.append(obj['Key'])
        return all_keys

    def _download(self, object_key: str, local_file_path: str):
        self.__s3.download_file('flatfiles',
                                object_key,
                                local_file_path)

    def _get_keys_of_kind(self, kind: str):
        filter_kind = lambda key: kind in key
        filter_5_years = lambda key: PolygonS3Access.key_is_within_given_years(key, self.years_filter)
        result = list(self._get_all_keys())
        result = list(filter(filter_kind, result))
        result = list(filter(filter_5_years, result))
        return result

    def _download_missing_agg(self, func_get_all_keys, kind: str, download_dir: str, dry_run: bool = False):
        known_keys = func_get_all_keys()
        present_files = [f for f in os.listdir(download_dir) if f.endswith('.gz')]
        present_keys = [self._full_filename_to_key(f, kind=kind) for f in present_files]
        missing_keys = list(set(known_keys) - set(present_keys))
        missing_keys.sort()

        for idx, agg in enumerate(missing_keys, 1):
            print(f"Downloading entry {idx}/{len(missing_keys)}: {agg}")
            if not dry_run:
                self.download(agg, download_dir)