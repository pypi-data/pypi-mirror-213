from __future__ import annotations
import boto3
from pathlib import Path
import os
from lru import LRU

class FileFetcher:
    def __init__(self, aws_key_id:str, aws_key_secret:str, s3_bucket:str, s3_prefix:str, local_dir:str, cache_size: int):
        '''
        A file fetcher that first checks if the file is on the disk, and if not,
        downloads it from s3.
        It also removes files that are no longer needed from the disk.

        TODO: Support running multiple instances of the file fetcher in different processes.
        '''
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix[:-1] if s3_prefix.endswith('/') else s3_prefix
        self.local_dir = local_dir
        self.cache_size = cache_size
        def remove_file_by_path(file_key:str, file_path: str):
            try:
                os.unlink(file_path)
            except Exception as e:
                print(e)
        self.lru = LRU(self.cache_size, callback=remove_file_by_path)
        self.s3 = boto3.client('s3', aws_access_key_id=aws_key_id, aws_secret_access_key=aws_key_secret)
    
    def get_file(self, file_key):
        '''
        Gets the file as bytesfrom the disk if it exists, otherwise downloads it from s3.
        '''
        file_key = file_key[1:] if file_key.startswith('/') else file_key
        # Check if the file is on the disk
        file_path = self.ensure_exists(file_key)
        
        if file_path is None:
            return None
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def ensure_exists(self, file_key):
        '''
        Ensures that the file exists on the disk.
        '''
        file_key = file_key[1:] if file_key.startswith('/') else file_key
        # Check if the file is on the disk
        file_path = self._get_local_file_path(file_key)
        # Use lru to trigger file removal if needed
        self.lru[file_key] = file_path

        # Check if the file exists on the disk
        if os.path.exists(file_path):
            return file_path
        
        # Download the file from s3
        print(f'Downloading file {file_key} to {file_path}')
        try:
            self.s3.download_file(self.s3_bucket, f'{self.s3_prefix}/{file_key}', file_path)
            return file_path
        except Exception as e:
            print(e)
            return None
    
    def remove_file(self, file_key):
        '''
        Removes the file from the disk.

        In most cases, you don't have to explicity call this method, as the LRU will
        automatically remove files from the disk when needed.
        '''
        print(f'Removing file {file_key}')
        file_path = self._get_local_file_path(file_key)
        try:
            os.unlink(file_path)
        except Exception as e:
            print(e)
    
    def _get_local_file_path(self, file_key):
        '''
        Gets the local file path.
        '''
        return str(Path(self.local_dir).joinpath(file_key))