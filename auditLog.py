from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random

from util import util

shortCutDateIDs = ['1', '2', '3', '4', '5',
                   '6', '7', '8', '9', '10', '11', '12']
shortCutName = 'rangePickerShortcut{id}'


class TestAuditLog(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.logger = util.get_logger()

    def test(self):
        def autoPage(self):
            nextPageEl = self.driver.find_element(
                By.CLASS_NAME, 'ant-table-pagination').find_element(By.CLASS_NAME, 'ant-pagination-next')
            a = nextPageEl.get_attribute('aria-disabled')
            if a == 'false':
                nextPageEl.click()
                sleep(3)

        self.driver.get('http://172.16.6.62:8080/login')
        sleep(1)
        self.driver.find_element(
            By.ID, 'userID').send_keys('selenium_test1')
        sleep(1)
        self.driver.find_element(By.ID, 'password').send_keys('123456')
        sleep(1)
        self.driver.find_element(By.ID, 'login').click()
        sleep(2)
        self.driver.find_element(By.NAME, 'menu.audit.log').click()
        sleep(3)
        for d in shortCutDateIDs:
            self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
            sleep(2)
            self.driver.find_element(
                By.NAME, shortCutName.format(id=d)).click()
            sleep(2)
            self.driver.find_element(By.NAME, 'auditLogSearchBtn').click()
            sleep(5)
        # autoPage(self)
        # autoPage(self)

        self.driver.quit()


if __name__ == '__main__':
    case = TestAuditLog()
    case.test()
