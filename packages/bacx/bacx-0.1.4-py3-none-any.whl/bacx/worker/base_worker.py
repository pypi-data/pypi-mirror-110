import json
import logging
import os
import random
import reprlib
import sys
import time
from threading import Lock

import requests
from google.cloud.pubsub_v1.subscriber.message import Message
from requests import Response

from bacx.messages.subscriber import the_subscriber
from bacx.worker.types import TLOG, JobDescription, JobResult, PubResponse


class BaseWorker:
    def __init__(self, job_type: str, load_fn: callable, predict_fn: callable):
        """
        :param job_type: name of the subscribed job type
        :param load_fn: function that gets no arguments and returns X
        :param predict_fn: function that gets X and JobDescription and returns JobResult
        """
        self.API_URL = os.environ.get("API_URL", "http://api:5000")
        self.WORKER_USER = os.environ.get("WORKER_USER", "worker")
        self.WORKER_AUTH = os.environ.get("WORKER_AUTH", "")
        # TODO (jano) move to some kind of config
        self.RETRY_INTERVAL = 3

        self.job_type = job_type
        self.logger = logging.getLogger(self.__class__.__name__)
        self.load_fn = load_fn
        self.predict_fn = predict_fn
        self.models = None
        self.id = f"{random.getrandbits(24):06x}"
        self.work_lock = Lock()

    def _handle_action(
        self,
        action: str,
        data: dict,
        logs: TLOG,
        job: JobDescription,
        work_id: str,
        timeout: int,
        allow_retries: int = 0,
    ):
        args = {"key": job.key, "worker": work_id}
        if action in ["lease", "refresh"]:
            args["timeout"] = timeout
        if logs is not None:
            args["logs"] = logs
        try:
            # TODO (jano) maybe use job.version instead of f
            response = requests.put(
                f"{self.API_URL}/api/f/jobs/{job.job_id}/worker/",
                auth=(self.WORKER_USER, self.WORKER_AUTH),
                data={**data, "action": action, "args": json.dumps(args)},
            )
        except Exception as e:
            response = Response()
            response.status_code = 500
            response._content = str(e).encode()

        if response.status_code != 200:
            self.logger.warning(
                f"Request for action {action} failed ({allow_retries} retries remaining). "
                f"{response.status_code}: {response.content[:32]}"
            )
            if allow_retries > 0:
                time.sleep(self.RETRY_INTERVAL)
                return self._handle_action(action, data, logs, job, work_id, timeout, allow_retries - 1)
            return PubResponse.NACK
        self.logger.debug(f"Request for action {action}({args}) returned {response.content}")
        return PubResponse(json.loads(response.content)["response"])

    def _get_result_logs_and_data(self, result: JobResult, run_time: float):
        if not result or result.error:
            error = result.error if result else "Something went wrong"
            self.logger.error(f"Failed job: {error}...")
            return [f"Job failed after {run_time:.1f}s", error], {
                "status": "failed",
                "output_data": "",
                "output_files": "",
            }
        self.logger.info(f"Reporting result {reprlib.repr(result)}...")
        return f"Job succeeded after {run_time:.1f}s", {
            "status": "success",
            "output_data": json.dumps(result.output_data),
            "output_files": json.dumps(result.output_files),
        }

    def _handle_message(self, message: Message):
        with self.work_lock:  # handle at most one message at a time
            response = self._work(message)
            if response == PubResponse.OK:
                self.logger.info(f"Done with message {message.message_id}")
            if response == PubResponse.NACK:
                message.nack()
            else:
                message.ack()

    def _work(self, message: Message) -> PubResponse:
        raise NotImplementedError

    def run(self):
        # TODO (jano) think about this
        # remove any leftovers from previous runs
        # os.makedirs(WORKER_DATA_PATH, exist_ok=True)
        # os.makedirs(WORKER_MODEL_PATH, exist_ok=True)
        # shutil.rmtree(WORKER_DATA_PATH)
        # os.makedirs(WORKER_DATA_PATH)

        try:
            self.models = self.load_fn()
        except Exception as e:
            logging.error(e)
            logging.error(f"Unable to load worker for type {self.job_type}. Giving up.")
            sys.exit(1)

        logging.info("Models loaded")
        the_subscriber.blocking_subscribe(self.job_type.replace("_", "-"), self._handle_message)
