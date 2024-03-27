from flask import request, jsonify
from . import constants as const
from app import webserver

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    try:
        job_id = int(job_id)
    except:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    
    if webserver.tasks_runner.job_id <= job_id or job_id < 0:
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    if webserver.tasks_runner.jobs[job_id]["status"] == "done":
        with open(f"results/{job_id}") as f:
            result = f.read()
            return jsonify({"status": "done", "data": json.loads(result)})
    else:
        return jsonify({'status': 'running'})

def request_processor(request, task):
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    data = request.json
    data["task"] = task
    code, job_id = webserver.tasks_runner.submit_task(**data)

    return jsonify({
        "message": "Received data successfully",
        "status": "error" if code else "success",
        "job_id": job_id
    })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    return request_processor(request, const.STATES_MEAN)

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    return request_processor(request, const.STATE_MEAN)

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    return request_processor(request, const.BEST5)

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    return request_processor(request, const.WORST5)

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    return request_processor(request, const.GLOBAL_MEAN)

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    return request_processor(request, const.DIFF_FROM_MEAN)

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    return request_processor(request, const.STATE_DIFF_FROM_MEAN)

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
