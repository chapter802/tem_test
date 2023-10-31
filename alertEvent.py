from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from seleniumwire import webdriver
import random
import moment
from util import util
from configParams import alertLevels, alertTypes, alertEventStatus, shortCutDateIDs, shortCutName, apiDict

cusDate = [moment.now().format('YYYY-MM-DD'),
           moment.now().format('YYYY-MM-DD')]

# 测试用例中的接口
apiKeyArr = ['queryAlertEventList']


class TestAlert(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test(self):

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))

        def closeModal(self):
            try:
                notiCLoseEle = self.driver.find_element(
                    By.CLASS_NAME, 'ant-notification-notice-close-x')
            except:
                notiCLoseEle = None

            try:
                drawerCusCloseBtn = self.driver.find_element(
                    By.CLASS_NAME, 'ant-drawer-body').find_element(By.NAME, 'drawerCusCloseBtn')
            except:
                drawerCusCloseBtn = None

            try:
                modalCloseBtn = self.driver.find_element(
                    By.CLASS_NAME, 'ant-modal-footer').find_element(By.CLASS_NAME, 'ant-btn-default')
            except:
                modalCloseBtn = None

            if notiCLoseEle != None:
                notiCLoseEle.click()
            elif drawerCusCloseBtn != None:
                drawerCusCloseBtn.click()
            elif modalCloseBtn != None:
                modalCloseBtn.click()

        def __selectDate(self):
            randomDate = random.choice(shortCutDateIDs)
            self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
            webWaitEle(self, (
                By.NAME, shortCutName.format(id=randomDate))).click()

        self.driver.get('http://172.16.6.62:8080/login')
        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        webWaitEle(self, (By.NAME, 'menu.alert')).click()
        webWaitEle(self, (By.NAME, 'menu.alert.event')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAlertEventList'], closeModal)

        for x in alertLevels:
            webWaitEle(self, (
                By.NAME, 'alertEventLevelSelect')).click()

            webWaitEle(self, (By.NAME, x)).click()
            webWaitEle(self, (
                By.NAME, 'alertEventSearchBtn')).click()
            util.getRequsetInfo(
                self, self.driver, apiDict['queryAlertEventList'], closeModal)
            sleep(1)

            for y in alertTypes:
                webWaitEle(self, (
                    By.NAME, 'alertEventTypeSelect')).click()
                webWaitEle(self, (By.NAME, y)).click()
                __selectDate(self)
                webWaitEle(self, (
                    By.NAME, 'alertEventSearchBtn')).click()
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryAlertEventList'], closeModal)
                sleep(1)
                for z in alertEventStatus:
                    webWaitEle(self, (
                        By.NAME, 'alertEventStatusSelect')).click()

                    webWaitEle(self, (By.NAME, z)).click()
                    sleep(3)
                    webWaitEle(self, (
                        By.NAME, 'alertEventSearchBtn')).click()
                    util.getRequsetInfo(
                        self, self.driver, apiDict['queryAlertEventList'], closeModal)
                    

        sleep(2)
        self.driver.quit()


if __name__ == '__main__':
    # test()
    case = TestAlert()
    case.test()
