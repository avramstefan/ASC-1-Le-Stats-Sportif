from threading import Thread, Event, Condition
from .data_ingestor import DataIngestor
from . import constants as const
from queue import Queue
from .tasks import *

import numpy as np
import time
import json
import os

class ThreadPool:
    def __init__(self, data_ingestor: DataIngestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        
        try:
            self.num_threads = int(os.getenv("TP_NUM_OF_THREADS"))
        except:
            self.num_threads = os.cpu_count()

        self.job_id = 0
        self.jobs = {}
        self.job_condition = Condition()
        self.data_ingestor = data_ingestor
        
        self.tasks = Queue()
        self.threads = [TaskRunner(self, data_ingestor) for _ in range(self.num_threads)]

        self.processing_on = True # Flag to indicate if the thread pool is processing tasks

    def graceful_shutdown(self):
        self.processing_on = False

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
        try:
            self.validate_task(**kwargs)
        except ValueError as e:
            return str(e), -1
        
        with self.job_condition:
            current_job_id = self.job_id
            self.job_id += 1
            
        self.jobs[current_job_id] = {
            "status": "running",
        }

        self.tasks.put((current_job_id, kwargs))
        return 0, current_job_id

    def validate_task(self, **kwargs):
        if "question" not in kwargs:
            raise ValueError("Question not provided")

        if kwargs["question"] not in self.data_ingestor.data.keys():
            raise ValueError("Invalid question")

class TaskRunner(Thread):
    def __init__(self, pool: ThreadPool, data_ingestor: DataIngestor):
        super().__init__()
        self.pool = pool
        self.data_ingestor = data_ingestor
        self.processing_on = True

        self.set_task_mapper()
        self.start()

    def write_result(self, job_id, result):
        with open(f"results/{job_id}", "w") as f:
            f.write(json.dumps(result))

        self.pool.jobs[job_id]["status"] = "done"

    def set_task_mapper(self):
        self.task_mapper = {}
        constants = const.get_task_constants()

        for _, task in enumerate(constants):
            self.task_mapper[task[1]] = globals()[task[0]]

    def graceful_shutdown(self):
        self.processing_on = False

    def run(self):
        while self.processing_on:
            # Get a task from the queue using block flag to wait until a task is available and avoid busy waiting
            task = self.pool.tasks.get(block=True)

            if task == const.GRACEFUL_SHUTDOWN:
                self.graceful_shutdown()
                continue

            # Execute task
            data = self.task_mapper[task[1]["task"]](self.data_ingestor, task[0], task[1])
            
            # Write result
            self.write_result(task[0], data)
            