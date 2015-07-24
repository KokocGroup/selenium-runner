# -*- coding: utf8 -*-
from celery import Celery
app = Celery()
app.config_from_object('settings')

import google_analitycs
