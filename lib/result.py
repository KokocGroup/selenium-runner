# -*- coding: utf8 -*-
import base64
import os
import settings


def create_ga_screen_result(task_uid):
    result_path = os.path.join(settings.RESULTS_FOLDER, task_uid)
    result = {}

    for file_name in os.listdir(result_path):
        if '.png' in file_name:
            file_path = os.path.join(result_path, file_name)
            screen_type = file_name.split('.png')[0]
            with open(file_path) as f:
                content = f.read()
                result[screen_type] = base64.b64encode(content)

    return result
