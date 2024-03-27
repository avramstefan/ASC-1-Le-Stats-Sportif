# Tasks
STATES_MEAN = 1
STATE_MEAN = 2
BEST5 = 3
WORST5 = 4
GLOBAL_MEAN = 5
DIFF_FROM_MEAN = 6
STATE_DIFF_FROM_MEAN = 7
MEAN_BY_CATEGORY = 8
STATE_MEAN_BY_CATEGORY = 9
GRACEFUL_SHUTDOWN = 10

def get_task_constants():
    return [
        ("states_mean", STATES_MEAN),
        ("state_mean", STATE_MEAN),
        ("best5", BEST5),
        ("worst5", WORST5),
        ("global_mean", GLOBAL_MEAN),
        ("diff_from_mean", DIFF_FROM_MEAN),
        ("state_diff_from_mean", STATE_DIFF_FROM_MEAN),
        ("mean_by_category", MEAN_BY_CATEGORY),
        ("state_mean_by_category", STATE_MEAN_BY_CATEGORY),
    ]