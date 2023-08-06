from cached_file_fetcher import FileFetcher
import unittest
import os
from pathlib import Path


class MockS3:
    def __init__(self):
        self.download_called_times = 0

    def download_file(self, bucket: str, key: str, file_path: str):
        self.download_called_times += 1
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        # Write some dummy content to the file
        with open(file_path, 'w') as f:
            f.write(f'{file_path}__{self.download_called_times}')


class TestFileFetcher(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = str(Path(__file__).parent.joinpath('testdata'))
        # Remove test data folder recursively if exists
        if os.path.exists(self.test_data_folder):
            os.system(f'rm -rf {self.test_data_folder}')
        # mkdir if not exists
        Path(self.test_data_folder).mkdir(parents=True, exist_ok=True)
        self.file_fetcher = FileFetcher(
            aws_key_id='something', aws_key_secret='somesecret', s3_bucket='somebucket', s3_prefix='somepath',
            local_dir=self.test_data_folder, cache_size=1)
        self.mock_s3 = MockS3()
        self.file_fetcher.s3 = self.mock_s3

    def test_fetch_file(self):
        content1 = self.file_fetcher.get_file('path1/name1')
        self.assertEqual(content1.decode('utf-8'), str(Path(self.test_data_folder).joinpath('path1/name1__1')))
        content2 = self.file_fetcher.get_file('path1/name1')
        self.assertEqual(content2.decode('utf-8'), str(Path(self.test_data_folder).joinpath('path1/name1__1')))
        file_path_1 = content2.decode('utf-8').split('__')[0]
        self.assertTrue(os.path.exists(file_path_1))
        content3 = self.file_fetcher.get_file('path1/name2')
        file_path_2 = content3.decode('utf-8').split('__')[0]
        self.assertEqual(content3.decode('utf-8'), str(Path(self.test_data_folder).joinpath('path1/name2__2')))
        self.assertFalse(os.path.exists(file_path_1))
        self.assertTrue(os.path.exists(file_path_2))
        content4 = self.file_fetcher.get_file('path1/name1')
        self.assertEqual(content4.decode('utf-8'), str(Path(self.test_data_folder).joinpath('path1/name1__3')))
        self.assertTrue(os.path.exists(file_path_1))
        self.assertFalse(os.path.exists(file_path_2))

    def test_ensure_file_exists(self):
        self.assertFalse(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name1'))))
        self.file_fetcher.ensure_exists('path1/name1')
        self.assertTrue(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name1'))))
        self.file_fetcher.ensure_exists('path1/name1')
        self.assertTrue(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name1'))))
        self.assertFalse(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name2'))))
        self.file_fetcher.ensure_exists('path1/name2')
        self.assertFalse(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name1'))))
        self.assertTrue(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name2'))))
        self.file_fetcher.ensure_exists('path1/name2')
        self.assertTrue(os.path.exists(str(Path(self.test_data_folder).joinpath('path1/name2'))))


if __name__ == '__main__':
    unittest.main()
