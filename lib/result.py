# -*- coding: utf8 -*-
import base64
import os
import settings


def create_ga_screen_result(task_uid):
    result_path = os.path.join(settings.RESULTS_FOLDER, task_uid)
    result = {}
    for screen_type in 'organic', 'month_comparison', 'year_comparison', 'segment':
        file_path = os.path.join(result_path, screen_type + '.png')
        if os.path.exists(file_path):
            with open(file_path) as f:
                content = f.read()
                result[screen_type] = base64.b64encode(content)

    return result
