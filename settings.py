# -*- coding: utf8 -*-
import os

BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
# CELERY_ALWAYS_EAGER = True

# Отключил работу через проксю, так как Google ее детектит как робота.
PROXY = '31.184.200.129:8888'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
RESULTS_FOLDER = os.path.join(PROJECT_PATH, 'results')
DEBUG = False
