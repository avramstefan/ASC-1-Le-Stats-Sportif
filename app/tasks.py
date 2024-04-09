""" Module for processing data based on the task provided. """

import numpy as np

def states_mean(data_obj:dict, task:dict) -> dict:
    """
        Calculate the mean of the data values for each state.
    """
    processed_data = {
        # Calculate the mean of the data values for each state
        state: np.mean([float(entry["DataValue"])
        for entry in data_obj.data[task["question"]][state]])
        for state in data_obj.data[task["question"]]
    }

    return dict(sorted(processed_data.items(), key=lambda x: x[1]))

def state_mean(data_obj:dict, task:dict) -> dict:
    """
        Calculate the mean of the data values for the state.
    """
    if "state" not in task:
        raise ValueError("State not provided")

    processed_data = {
        # Calculate the mean of the data values for the state
        task["state"]: np.mean([float(entry["DataValue"])
        for entry in data_obj.data[task["question"]][task["state"]]])
    }

    return processed_data

def best5(data_obj:dict, task:dict) -> dict:
    """
        Calculate the best 5 states based on the data values for the question.
    """
    processed_data = {
        # Calculate the mean of the data values for each state
        state: np.mean([float(entry["DataValue"])
        for entry in data_obj.data[task["question"]][state]])
        for state in data_obj.data[task["question"]]
    }

    best_is_max = False
    if task['question'] in data_obj.questions_best_is_max:
        best_is_max = True

    return dict(sorted(processed_data.items(), key=lambda x: x[1], reverse=best_is_max)[0:5])

def worst5(data_obj:dict, task:dict) -> dict:
    """
        Calculate the worst 5 states based on the data values for the question.
    """
    processed_data = {
        # Calculate the mean of the data values for each state
        state: np.mean([float(entry["DataValue"])
        for entry in data_obj.data[task["question"]][state]])
        for state in data_obj.data[task["question"]]
    }

    best_is_min = False
    if task['question'] in data_obj.questions_best_is_min:
        best_is_min = True

    return dict(sorted(processed_data.items(), key=lambda x: x[1], reverse=best_is_min)[0:5])

def global_mean(data_obj:dict, task:dict) -> dict:
    """
        Calculate the global mean of the data values for the question.
    """
    values = []
    for state in data_obj.data[task["question"]]:
        values.extend([float(entry["DataValue"])
            for entry in data_obj.data[task["question"]][state]])

    global_mean_data = {
        "global_mean": np.mean(values)
    }

    return global_mean_data

def diff_from_mean(data_obj:dict, task:dict) -> dict:
    """
        Calculate the difference between the global mean and
        the mean of the data values for each state.
    """
    global_mean_data = global_mean(data_obj, task)["global_mean"]
    states_data = states_mean(data_obj, task)

    processed_data = {
        state: global_mean_data - mean
        for state, mean in states_data.items()
    }

    return processed_data

def state_diff_from_mean(data_obj:dict, task:dict) -> dict:
    """
        Calculate the difference between the global mean and
        the mean of the data values for the state.
    """
    global_mean_data = global_mean(data_obj, task)["global_mean"]
    state_mean_data = state_mean(data_obj, task)[task["state"]]

    processed_data = {
        task["state"]: global_mean_data - state_mean_data
    }

    return processed_data

def mean_category_by_state_helper(data_obj, task, state, processed_data) -> dict:
    """
        Helper function to calculate the mean of the data values for each state,
        grouped by category and category value.
    """
    for entry in data_obj.data[task["question"]][state]:
        category = entry["StratificationCategory1"]

        if category is None or category == "":
            continue

        category_value = entry["Stratification1"]
        data_value = float(entry["DataValue"])

        tuple_key = (state, category, category_value)
        dumped_tuple_key = str(tuple_key)

        if dumped_tuple_key not in processed_data:
            processed_data[dumped_tuple_key] = [data_value]
        else:
            processed_data[dumped_tuple_key].append(data_value)
    return processed_data

def mean_by_category(data_obj:dict, task:dict) -> dict:
    """
        Calculate the mean of the data values for each state,
        grouped by category and category value.
    """
    processed_data = {}
    for state in data_obj.data[task["question"]]:
        processed_data = mean_category_by_state_helper(data_obj, task, state, processed_data)

    processed_data = {
        key: np.mean(values)
        for key, values in processed_data.items()
    }

    # sort processed data tuple keys by the first element of the tuple, then the second
    processed_data = dict(sorted(processed_data.items(),
            key=lambda x: (tuple(eval(x[0]))[0], tuple(eval(x[0]))[1], tuple(eval(x[0]))[2])))

    return processed_data

def state_mean_by_category(data_obj:dict, task:dict) -> dict:
    """
        Calculate the mean of the data values for the state,
        grouped by category and category value.
    """
    if "state" not in task:
        raise ValueError("State not provided")

    processed_data = mean_category_by_state_helper(data_obj, task, task["state"], {})

    processed_data = {
        task["state"]: {
            str(tuple(list(tuple(eval(key)))[1:])): np.mean(values)
            for key, values in processed_data.items()
    }}

    # sort processed data tuple keys by the first element of the tuple, then the second
    processed_data[task["state"]] = dict(sorted(processed_data[task["state"]].items(),
            key=lambda x: (tuple(eval(x[0]))[0], tuple(eval(x[0]))[1])))

    return processed_data
