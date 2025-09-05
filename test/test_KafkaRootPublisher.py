import os
import unittest

from app.publisher.KafkaRootPublisher import _get_list_files, _transform_csvgz_to_StockAggregate


class TestKafkaRootPublisher(unittest.TestCase):
    current_dir = os.path.join(os.getcwd(), "test")  # should be /test folder
    test_file = "2020-08-24.csv.gz"
    test_file_full_path = [os.path.join(current_dir, test_file)]

    def test__get_list_files(self):
        expect = self.test_file_full_path
        actual = _get_list_files(self.current_dir)
        print(actual)
        self.assertEqual(expect, actual)

    def test__transform_csvgz_to_StockAggregate(self):
        expect = 8769
        actual = _transform_csvgz_to_StockAggregate(self.test_file_full_path[0])
        self.assertEqual(len(actual), expect)


if __name__ == '__main__':
    unittest.main()
