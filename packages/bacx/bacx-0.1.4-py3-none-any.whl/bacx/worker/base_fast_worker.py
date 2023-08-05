import logging
import random
import time
import traceback

from bacx.messages.subscriber import TMessage
from bacx.worker.base_worker import BaseWorker
from bacx.worker.types import JobDescription, JobResult, PubResponse


class FastWorker(BaseWorker):
    # Temporary constant, TODO (jano) move somewhere else
    PROCESSING_TIMEOUT = 20

    def _work(self, message: TMessage) -> PubResponse:
        self.logger.info(f"Received message {message}")
        if self.models is None:
            raise Exception("You must load models before running predictions")

        message.modify_ack_deadline(self.PROCESSING_TIMEOUT)
        job = JobDescription.from_message(message)
        work_id = f"{self.id}-{random.getrandbits(32):08x}"
        start_time = time.perf_counter()
        try:
            result = self.predict_fn(self.models, job)
        except Exception as e:
            logging.info(f"Error in prediction for {job.job_id}: {e}")
            result = JobResult(output_data={}, output_files=[], error=traceback.format_exc())
        end_time = time.perf_counter()

        logs, data = self._get_result_logs_and_data(result, end_time - start_time)
        return self._handle_action("fast_finish", data, logs, job, work_id, self.PROCESSING_TIMEOUT, allow_retries=2)
