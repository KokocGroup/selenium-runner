# -*- coding: utf8 -*-
from celery import Task
from pyvirtualdisplay import Display
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver

import settings


class SeleniumTask(Task):

    abstract = True
    cached_browser = display = None

    @property
    def browser(self):
        if not self.display:
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()

        if self.cached_browser is None:
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': settings.PROXY,
                'sslProxy': settings.PROXY
            })
            profile = webdriver.FirefoxProfile()
            profile.set_preference('webdriver.firefox.bin', 'firefox')
            self.cached_browser = webdriver.Firefox(profile, proxy=proxy)
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
