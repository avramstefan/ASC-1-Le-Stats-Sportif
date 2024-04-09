""" Worker thread pool to process tasks. """

import json
import os

from threading import Thread, Condition
from queue import Queue
from .data_ingestor import DataIngestor
from . import constants as const
from .tasks import *

class ThreadPool:
    """
        Worker thread pool (load balancer) to process tasks.
    """
    def __init__(self, data_ingestor: DataIngestor):
        try:
            self.num_threads = int(os.getenv("TP_NUM_OF_THREADS"))
        except TypeError:
            self.num_threads = os.cpu_count()

        self.job_id = 0
        self.jobs = {}
        self.job_condition = Condition()
        self.data_ingestor = data_ingestor

        self.tasks = Queue()
        self.threads = [TaskRunner(self, data_ingestor) for _ in range(self.num_threads)]

        self.processing_on = True # Flag to indicate if the thread pool is processing tasks

    def graceful_shutdown(self):
        """
            Gracefully shutdown the ThreadPool.
        """
        self.processing_on = False

        # Send a signal to all threads to shutdown
        for _ in range(self.num_threads):
            self.tasks.put(const.GRACEFUL_SHUTDOWN)

        for thread in self.threads:
            thread.join()

    """
        Return:
            0, job_id: if the task was successfully submitted
            error_message, -1: if the task was not successfully submitted
    """
    def submit_task(self, **kwargs):
        """
            Submit a task to the ThreadPool.
        """
        try:
            self.validate_task(**kwargs)
        except ValueError as e:
            return str(e), -1

        # Assign a job_id to the task,
        # using a lock to ensure safety in assigning job_id
        with self.job_condition:
            current_job_id = self.job_id
            self.job_id += 1

        self.jobs[current_job_id] = {
            "status": "running",
        }

        # Put the task in the queue (blocking operation)
        self.tasks.put((current_job_id, kwargs))
        return 0, current_job_id

    def validate_task(self, **kwargs):
        """
            Validate the task, checking if it contains 'question' key.
        """
        if "question" not in kwargs:
            raise ValueError("Question not provided")

        if kwargs["question"] not in self.data_ingestor.data.keys():
            raise ValueError("Invalid question")

class TaskRunner(Thread):
    """
        Worker thread to process tasks.
    """
    def __init__(self, pool: ThreadPool, data_ingestor: DataIngestor):
        super().__init__()
        self.pool = pool
        self.data_ingestor = data_ingestor
        self.processing_on = True

        self.set_task_mapper()
        self.start()

    def write_result(self, job_id, result):
        """
            Write the result to a file.
        """
        with open(f"results/{job_id}", "w", encoding="utf-8") as f:
            f.write(json.dumps(result))

        self.pool.jobs[job_id]["status"] = "done"

    def set_task_mapper(self):
        """
            Map the task name to the function that processes the task.
        """
        self.task_mapper = {}
        constants = const.get_task_constants()

        for _, task in enumerate(constants):
            self.task_mapper[task[1]] = globals()[task[0]]

    def graceful_shutdown(self):
        """
            This function is called when the server is shutting down.
        """
        self.processing_on = False

    def run(self):
        """
            This function is the main function for the TaskRunner thread.
        """
        while self.processing_on:
            # Get a task from the queue using block flag to wait until
            # a task is available and avoid busy waiting
            task = self.pool.tasks.get(block=True)

            if task == const.GRACEFUL_SHUTDOWN:
                self.graceful_shutdown()
                continue

            # Execute task
            data = self.task_mapper[task[1]["task"]](self.data_ingestor, task[1])

            # Write result
            self.write_result(task[0], data)
