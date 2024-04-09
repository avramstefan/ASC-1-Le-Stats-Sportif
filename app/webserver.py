"""
    This module is the entry point of the application.
    It initializes the Flask web server and the data ingestor.
"""

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.logs.log import instantiate_logger

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(webserver.data_ingestor)

webserver.job_counter = 1

logger = instantiate_logger()
