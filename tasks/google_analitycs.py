# -*- coding: utf8 -*-
import os
import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from lib.util import get_local_month
import settings
from tasks.base import SeleniumTask


class GAScreenMaker(SeleniumTask):

    @property
    def result_dir(self):
        return os.path.join(settings.RESULTS_FOLDER, self.request.id)

    def select_comparison(self, comparison_type):
        compare_select_element = self.browser.find_element_by_class_name('ID-datecontrol-compare-shortcuts')
        compare_select = Select(compare_select_element)
        compare_select.select_by_value(comparison_type)
        self.browser.find_element_by_class_name('ACTION-apply').click()

    def run(self, login, password, counter, profile, start_date, end_date):
        os.mkdir(self.result_dir)
        self.browser.implicitly_wait(1)
        self.browser.get('https://accounts.google.com')
        self.browser.find_element_by_id('Email').send_keys(login + Keys.ENTER)
        self.browser.find_element_by_id('Passwd').send_keys(password + Keys.ENTER)
        time.sleep(1)
        self.browser.get('https://www.google.com/analytics/web/#report/acquisition-channels')
        WebDriverWait(self.browser, 30).until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Organic Search')]"))).click()
        time.sleep(3)
        self.browser.find_element_by_class_name('_GAJZ').click()  # выбор дат
        date_start_input = self.browser.find_element_by_class_name('TARGET-primary_start')
        date_start_input.clear()
        date_start_input.send_keys(get_ga_date(start_date))
        date_end_input = self.browser.find_element_by_class_name('TARGET-primary_end')
        date_end_input.clear()
        date_end_input.send_keys(get_ga_date(end_date))
        self.browser.find_element_by_class_name('ACTION-apply').click()

        time.sleep(3)

        self.remove_element_by_id('ID-newKennedyHeader')
        self.remove_element_by_id('ID-navPanelContainer')
        self.remove_element_by_id('ID-navToggle')
        self.remove_elements_by_class('ACTION-mouse', 'ID-rowTable')
        self.remove_elements_by_class('_GAGq')  # пагинация
        self.remove_elements_by_class('_GABxb')  # дата создания
        self.remove_element_by_id('ID-footerPanel')

        self.browser.set_window_size(1400, 870)
        self.browser.save_screenshot(os.path.join(self.result_dir, 'organic.png'))

        # меняем сравнение графиков на месяц
        self.browser.find_element_by_class_name('_GAJZ').click()
        self.browser.find_element_by_class_name('ID-date_compare_mode').click()
        self.select_comparison('previousperiod')
        self.browser.set_window_size(1500, 890)
        time.sleep(3)
        self.browser.save_screenshot(os.path.join(self.result_dir, 'month_comparison.png'))

        # меняем сравнение графиков на год
        self.browser.find_element_by_class_name('_GAJZ').click()
        self.select_comparison('previousyear')
        self.browser.set_window_size(1500, 890)
        time.sleep(3)
        self.browser.save_screenshot(os.path.join(self.result_dir, 'year_comparison.png'))


def get_ga_date(d):
    month = get_local_month(d.month)
    return u'{} {} {} г.'.format(d.day, month, d.year)
