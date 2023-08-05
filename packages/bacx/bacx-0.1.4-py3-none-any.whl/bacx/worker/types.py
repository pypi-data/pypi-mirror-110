import json
import os
from enum import Enum
from typing import List, NamedTuple, Optional, Tuple, Union

from google.cloud.pubsub_v1.subscriber.message import Message

from bacx.utils.dict_utils import replace_prefixed_values

"""
Common structure accepted by both Worker and API
"""


class JobDescription(NamedTuple):
    version: str
    type: str
    key: int
    job_id: str
    input_data: dict
    input_files: List[str]

    def set_input_files(self, input_files):
        return JobDescription(**{**self._asdict(), "input_files": input_files})

    @staticmethod
    def from_message(message: Message):
        data = json.loads(message.data.decode("utf8"))
        return JobDescription(
            version=data["version"],
            type=data["type"],
            key=data["key"],
            job_id=data["job_id"],
            input_data=data["input_data"],
            input_files=data["input_files"],
        )

    def to_message(self) -> bytes:
        return json.dumps(self._asdict()).encode("utf8")


class JobResult(NamedTuple):
    output_data: dict
    output_files: List[str]
    error: Optional[str] = None

    def transform_urls(self, old_path: str, bucket: str, new_path: str) -> "JobResult":
        """
        Output_files are changed from `<name>` to `<new_path><name>`
        Urls in output_data are changed from
            `<old_path><name>`
        to
            `<bucket><new_path><name>`

        :param old_path: ex. file://path/to/job_id/
        :param bucket: ex. gs://bucket_name/
        :param new_path: ex. club/date-job_id/
        :return: transformed JobResult
        """
        if not self.output_data or not self.output_files:
            return self
        if not old_path.endswith("/"):
            old_path = old_path + "/"
        url_map = {file: os.path.join(bucket, new_path, file) for file in self.output_files}
        return JobResult(
            output_files=[os.path.join(new_path, file) for file in self.output_files],
            output_data=replace_prefixed_values(self.output_data, old_path, url_map),
            error=self.error,
        )


class PubResponse(Enum):
    OK = "ok"
    ACK = "ack"
    NACK = "nack"


TLOG = Union[str, None, Tuple[Optional[str], Optional[str]]]
