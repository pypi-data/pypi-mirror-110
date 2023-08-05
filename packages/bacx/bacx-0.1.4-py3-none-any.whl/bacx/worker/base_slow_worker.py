import random
import time
import traceback
from threading import Thread

from google.cloud.pubsub_v1.subscriber.message import Message

from bacx.worker.base_worker import BaseWorker
from bacx.worker.types import JobDescription, JobResult, PubResponse


class ThreadWithReturnValue(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = JobResult(output_data={}, output_files=[], error="No target")

        self.id = f"{random.getrandbits(32):08x}"
        self._start_time = 0
        self.last_log_time = 0

    def get_run_time(self):
        return time.perf_counter() - self._start_time

    def run(self):
        self._start_time = time.perf_counter()
        try:
            if self._target:
                self._return = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._return = JobResult(output_data={}, output_files=[], error=traceback.format_exc())
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def join(self, timeout=None) -> JobResult:
        super().join(timeout=timeout)
        return self._return


class SlowWorker(BaseWorker):
    # Temporary constants: TODO (jano) move somewhere else
    PING_INTERVAL = 3
    PING_TIMEOUT = 30

    def _work(self, message: Message) -> PubResponse:
        self.logger.info(f"Received message {message}")
        if self.models is None:
            raise Exception("You must load models before running predictions")

        job = JobDescription.from_message(message)
        thread = ThreadWithReturnValue(target=self.predict_fn, args=(self.models, job))
        work_id = f"{self.id}-{thread.id}"
        response = self._handle_action("lease", {}, None, job, work_id, self.PING_TIMEOUT)
        if response != response.OK:
            return response
        thread.start()
        while thread.is_alive():
            message.modify_ack_deadline(self.PING_TIMEOUT)
            response = self._handle_action(
                "refresh",
                {},
                f"Running for {thread.get_run_time():.1f}s",
                job,
                work_id,
                self.PING_TIMEOUT,
                allow_retries=2,
            )
            if response != response.OK:
                # TODO kill process
                thread.join()
                return response
            time.sleep(self.PING_INTERVAL)

        message.modify_ack_deadline(self.PING_TIMEOUT)
        logs, data = self._get_result_logs_and_data(thread.join(), thread.get_run_time())
        return self._handle_action("finish", data, logs, job, work_id, self.PING_TIMEOUT, allow_retries=2)
