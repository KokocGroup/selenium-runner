# -*- coding: utf8 -*-
from celery import Task
from selenium import webdriver


class SeleniumTask(Task):
    abstract = True
    cached_browser = None

    @property
    def browser(self):
        if self.cached_browser is None:
            self.cached_browser = webdriver.Firefox()
        return self.cached_browser

    def remove_element_by_id(self, element_id):
        self.browser.execute_script("document.getElementById('{}').remove()".format(element_id))

    def remove_elements_by_class(self, elements_class, parent_id=None):
        self.browser.execute_script('''
        var parent = {};
        var elements = parent.getElementsByClassName('{}');
        while (elements.length) {{elements[0].remove()}};
        '''.format(
            "document.getElementById('{}')".format(parent_id) if parent_id else 'document',
            elements_class)
        )

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.browser.quit()
        self.cached_browser = None
