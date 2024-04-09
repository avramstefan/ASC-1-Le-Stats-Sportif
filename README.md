Name: Avram Cristian-Stefan
Group: 331CA

# ASC - Homework #1 - Le Stats Sportif

### Introduction
  This homework consists in a small backend application that provides a REST API for managing a sports statistics database. The application is written in Python using the Flask framework and the data is taken from a csv file.

### Webserver initialization
  The ```__init__.py``` file from ```app/``` is used for instantiating the ```routes.py``` and the Flask application (which can be find in ```webserver.py```). Here is also the place where the database is initialized and the data is loaded from the csv file.

### Tasks
  The tasks that the application can perform are found in the ```tasks.py``` file and
  their names may also be found in the ```constants.py``` file where they are stored as constants. In the latter file there is also a function that return all of these
  names. They are later used in ```task_runner.py``` - ```task_mapper()``` function
  to match the function names with the functions themselves.

  The workflow is the following:
* an endpoint is received in the ```routes.py``` and, using a generic_task function, the task is extracted from the request and sent to the ```task_runner.py``` file, to the
thread pool. There, the task is put in a Queue (which has blocking operations) and
it remains in the latter Queue until a thread is available to process it.
* the server is waiting for requests until /graceful_shutdown is called. When this happens, the server stops accepting new requests and waits for the current ones to finish. After that, the server is still running but cant accept new requests. This is possible because
the thread pool sends a graceful_shutdown signal to the threads and they finish their
current task and remaining tasks.

### Data
  The data is retrieved in ```data_ingestor.py``` and it stores just the most important features
  taken out from the given csv, like "Data_Value" and "State".

### Unit tests
  I have implemented some unit tests in the ```unittests/``` directory where I test the
  functionality of each task function, using a chunk of data from the csv file.

### Logging
  The logging is done in the ```app/logs/log.py``` file where I have implemented a custom logger that is used to print the input/output of the data
  through routes.


  