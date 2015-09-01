# -*- coding: utf8 -*-
import os
import re
import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from lib.util import get_local_month
import settings
from tasks.base import SeleniumTask


class GAScreenMakerException(Exception):
    pass


class GAScreenMaker(SeleniumTask):

    @property
    def result_dir(self):
        return os.path.join(settings.RESULTS_FOLDER, self.request.id)

    def select_comparison(self, comparison_type):
        compare_select_element = self.browser.find_element_by_class_name('ID-datecontrol-compare-shortcuts')
        compare_select = Select(compare_select_element)
        compare_select.select_by_value(comparison_type)
        self.browser.find_element_by_class_name('ACTION-apply').click()

    def __activate_date_panel(self):
        self.browser.find_element_by_xpath('//div[@id="ID-reportHeader-dateControl"]//td').click()

    def run(self, login, password, counter, start_date, end_date, segment_name):
        os.mkdir(self.result_dir)
        self.browser.implicitly_wait(1)
        self.browser.get('https://accounts.google.com')
        self.browser.find_element_by_id('Email').send_keys(login + Keys.ENTER)
        self.browser.find_element_by_id('Passwd').send_keys(password + Keys.ENTER)
        time.sleep(2)
        try:
            self.browser.find_element_by_xpath(u"//h1[@class='redtext' and contains(text(), "
                                               u"'В настоящее время обработать запрос невозможно')]")
            raise GAScreenMakerException("Banned IP")
        except NoSuchElementException:
            pass

        self.browser.get('https://www.google.com/analytics/web')
        WebDriverWait(self.browser, 30).until(expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "ID-viewList"))).click()  # режим списка
        # заходим в нужный профиль
        self.browser.find_element_by_xpath("//a[contains(@href, 'p{}/')]".format(counter)).click()
        time.sleep(3)
        # перейти в каналы
        profile_url_id = re.search('/(a\d+w\d+p\d+)/$', self.browser.current_url).group(1)
        self.browser.get('https://www.google.com/analytics/web/#report/acquisition-channels/' + profile_url_id)
        WebDriverWait(self.browser, 30).until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Organic Search')]"))).click()
        time.sleep(3)

        self.__activate_date_panel()
        date_start_input = self.browser.find_element_by_class_name('ID-datecontrol-primary-start')
        date_start_input.clear()
        date_start_input.send_keys(get_ga_date(start_date))
        date_end_input = self.browser.find_element_by_class_name('ID-datecontrol-primary-end')
        date_end_input.clear()
        date_end_input.send_keys(get_ga_date(end_date))
        self.browser.find_element_by_class_name('ACTION-apply').click()

        time.sleep(6)

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
        self.__activate_date_panel()
        self.browser.find_element_by_class_name('ID-date_compare_mode').click()
        self.select_comparison('previousperiod')
        self.browser.set_window_size(1500, 890)
        time.sleep(6)
        self.browser.save_screenshot(os.path.join(self.result_dir, 'month_comparison.png'))

        # меняем сравнение графиков на год
        self.__activate_date_panel()
        self.select_comparison('previousyear')
        time.sleep(6)
        self.browser.save_screenshot(os.path.join(self.result_dir, 'year_comparison.png'))

        if segment_name is not None:
            self.__activate_date_panel()
            self.browser.find_element_by_class_name('ID-date_compare_mode').click()
            self.browser.find_element_by_class_name('ACTION-apply').click()
            time.sleep(3)
            self.browser.find_element_by_class_name('ACTION-selectSegments').click()
            time.sleep(3)
            self.browser.find_element_by_xpath("//label[text()='Все сеансы']/../div/input").click()
            time.sleep(3)
            try:
                segment_input = self.browser.find_element_by_xpath("//label[text()='{}']/../div/input".format(segment_name))
            except NoSuchElementException:
                raise GAScreenMakerException("Not found segment: %s" % segment_name)
            segment_input.click()

            time.sleep(3)
            self.browser.find_element_by_xpath("//div[@id='ID-reportHeader-segmentPicker']//input[@value='Применить']").click()
            time.sleep(6)
            self.browser.save_screenshot(os.path.join(self.result_dir, 'segment.png'))


def get_ga_date(d):
    month = get_local_month(d.month)
    return u'{} {} {} г.'.format(d.day, month, d.year)
