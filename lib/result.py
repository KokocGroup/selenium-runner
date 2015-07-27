# -*- coding: utf8 -*-
import base64
import os
import settings


def create_ga_screen_result(task_uid):
    result_path = os.path.join(settings.RESULTS_FOLDER, task_uid)
    result = {}
    for screen_type in 'organic', 'month_comparison', 'year_comparison':
        with open(os.path.join(result_path, screen_type + '.png')) as f:
            content = f.read()
            result[screen_type] = base64.b64encode(content)
    return result
