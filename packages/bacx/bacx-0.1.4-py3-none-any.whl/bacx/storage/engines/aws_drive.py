from os.path import basename, isfile, join
from typing import BinaryIO, TextIO, Union

import boto3

from bacx.storage.engines.engine import StorageEngine


class AwsDrive(StorageEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._other is not None and "key_id" in self._other and "key" in self._other:
            self._aws = boto3.client(
                "s3", aws_access_key_id=self._other["key_id"], aws_secret_access_key=self._other["key"]
            )
        else:
            self._aws = boto3.client("s3")

    def upload_from_file(self, filepath: str, local_filepath: str) -> None:
        self._aws.upload_file(local_filepath, self._link, filepath)

    def download_to_file(
        self, filepath: str, local_file: str = None, local_dir: str = None, exist_ok: bool = True
    ) -> None:
        if local_dir is not None:
            local_file = join(local_dir, basename(filepath))
        if not exist_ok and isfile(local_file):
            raise FileExistsError(f"File `{local_file}` exists.")
        self._aws.download_file(self._link, filepath, local_file)
