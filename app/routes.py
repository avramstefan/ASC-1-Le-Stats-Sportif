"""
    This file contains the routes for the webserver. The routes are defined using Flask.
    Each task is sent to the task runner for processing. The task runner returns a job_id.
"""

import json
from flask import request, jsonify
from app.webserver import webserver as ws
from app.webserver import logger
from . import constants as const

@ws.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
        This function returns the result of the task with the given job_id.
    """

    try:
        job_id = int(job_id)
    except ValueError:
        logger.info(f"Invalid job_id - {job_id}")
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    if ws.tasks_runner.job_id <= job_id or job_id < 0:
        logger.info(f"Invalid job_id - {job_id}")
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    if ws.tasks_runner.jobs[job_id]["status"] == "done":
        with open(f"results/{job_id}", 'r', encoding='utf-8') as f:
            result = f.read()
            logger.info(f"Returned result for job_id - {job_id} (done)")
            return jsonify({"status": "done", "data": json.loads(result)})
    else:
        logger.info(f"Returned status for job_id - {job_id} (running)")
        return jsonify({'status': 'running'})

def generic_task(request, task):
    """
        This function is a generic function to process all the tasks.
    """

    if request.method != 'POST':
        logger.info(f"Received request with invalid method - {request.method}")
        return jsonify({"error": "Method not allowed"}), 405

    if ws.tasks_runner.processing_on is False:
        logger.info("Server is shutting down, can't accept new tasks")
        return jsonify({"job_id": -1, "reason": "Server is shutting down"})

    data = request.json
    data["task"] = task
    code, job_id = ws.tasks_runner.submit_task(**data)

    logger.info(f"Received data for task - {task} with job_id - {job_id}")
    return jsonify({
        "message": "Received data successfully",
        "status": "error" if code else "success",
        "job_id": job_id
    })

@ws.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
        This function is a route to process the states_mean task.
    """
    return generic_task(request, const.STATES_MEAN)

@ws.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
        This function is a route to process the state_mean task.
    """
    return generic_task(request, const.STATE_MEAN)

@ws.route('/api/best5', methods=['POST'])
def best5_request():
    """
        This function is a route to process the best5 task.
    """
    return generic_task(request, const.BEST5)

@ws.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
        This function is a route to process the worst5 task.
    """
    return generic_task(request, const.WORST5)

@ws.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
        This function is a route to process the global_mean task.
    """
    return generic_task(request, const.GLOBAL_MEAN)

@ws.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
        This function is a route to process the diff_from_mean task.
    """
    return generic_task(request, const.DIFF_FROM_MEAN)

@ws.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
        This function is a route to process the state_diff_from_mean task.
    """
    return generic_task(request, const.STATE_DIFF_FROM_MEAN)

@ws.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
        This function is a route to process the mean_by_category task.
    """
    return generic_task(request, const.MEAN_BY_CATEGORY)

@ws.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
        This function is a route to process the state_mean_by_category task.
    """
    return generic_task(request, const.STATE_MEAN_BY_CATEGORY)

@ws.route('/api/jobs', methods=['GET'])
def jobs():
    """
        This function returns the status of all the jobs.    
    """
    return jsonify(
        {
            "status": "done",
            "data": [
                {
                    f"job_id_{job_id}": job["status"],
                }
                for job_id, job in ws.tasks_runner.jobs.items()
            ]
        }
    )

@ws.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """
        This function returns the number of running jobs.
    """
    return jsonify(len(list(filter(
            lambda x: x["status"] == "running",
            ws.tasks_runner.jobs.values()
        ))))

@ws.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """
        This function is a route to shutdown the server gracefully.
    """
    ws.tasks_runner.graceful_shutdown()
    return jsonify({"status": "success"})

# You can check localhost in your browser to see what this displays
@ws.route('/')
@ws.route('/index')
def index():
    """ Display the available routes on the webserver """

    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the ws using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """ Get the defined routes on the webserver """

    routes = []
    for rule in ws.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
