from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import random
from seleniumwire import webdriver
import json
from util import util
from configParams import alertChannelTypes, alertChannelEnabled, alertChannelTempStr, apiDict

randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryAlertChannelList', 'createAlertChannel',
             'updateAlertChannel', 'testAlertChannelEmail', 'deleteAlertChannel']


class TestAlertChannel(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.logger = util.get_logger()

    def test(self):

        def webWaitEle(self, locator):
            # return WebDriverWait(self.driver, 20, 0.5).until(
            #     EC.presence_of_element_located(locator))
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

        self.driver.get('http://172.16.6.62:8080/login')
        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        webWaitEle(self, (By.NAME, 'menu.alert')).click()
        webWaitEle(self, (
            By.NAME, 'menu.alert.channel')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryAlertChannelList'], closeModal)

        # # 查询告警通道
        # for x in alertChannelTypes:
        #     webWaitEle(self, (
        #         By.NAME, 'alertChannelTypeSelect')).click()
        #     sleep(1)
        #     typeDropdown = self.driver.find_element(
        #         By.CLASS_NAME, 'alertChannelTypeDropdown')
        #     typeDropdown.find_element(By.NAME, x).click()
        #     webWaitEle(self, (By.NAME, 'alertChannelSearchBtn')).click()
        #     util.getRequsetInfo1(
        #         self, self.driver, apiDict['queryAlertChannelList'], closeModal)
        #     sleep(1)

        #     for y in alertChannelEnabled:
        #         webWaitEle(self, (
        #             By.NAME, 'alertChannelEnabledSelect')).click()
        #         sleep(1)
        #         enabledDropdown = self.driver.find_element(
        #             By.CLASS_NAME, 'alertChannelEnabledDropdown')
        #         enabledDropdown.find_element(By.NAME, y).click()
        #         webWaitEle(self, (By.NAME, 'alertChannelSearchBtn')).click()
        #         util.getRequsetInfo1(
        #             self, self.driver, apiDict['queryAlertChannelList'], closeModal)
        #         sleep(1)

        # 新增告警通道
        webWaitEle(self, (
            By.NAME, 'alertChannelAddBtn')).click()
        sleep(1)
        webWaitEle(self, (
            By.NAME, 'ruleIDs')).click()
        sleep(1)
        relateAlertRuleDropdown = self.driver.find_element(
            By.CLASS_NAME, 'relateAlertRuleDropdown')
        relateARItems = relateAlertRuleDropdown.find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        randomARItem = random.choice(relateARItems)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomARItem)
        sleep(1)
        randomARItem.click()
        sleep(1)
        randomARItem1 = random.choice(relateARItems)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomARItem1)
        sleep(1)
        randomARItem1.click()
        sleep(1)

        randomStr = util.get_random_string(6)
        webWaitEle(self, (
            By.ID, 'Name')).send_keys('selenium_test_' + randomStr)
        webWaitEle(self, (
            By.ID, 'SMTPAddress')).send_keys('smtp.qiye.aliyun.com:587')
        webWaitEle(self, (
            By.ID, 'SMTPUsername')).send_keys('tem-alert-noreply@pingcap.cn')
        webWaitEle(self, (
            By.ID, 'SMTPPassword')).send_keys('#LIeKu^oXB@30fT#')
        webWaitEle(self, (
            By.ID, 'Sender')).send_keys('#LIeKu^oXB@30fT#')
        webWaitEle(self, (
            By.ID, 'EmailFrom')).send_keys('tem-alert-noreply@pingcap.cn')
        webWaitEle(self, (
            By.ID, 'EmailTo')).send_keys('shenhaibo@pingcap.com.cn')
        webWaitEle(self, (
            By.ID, 'EmailSubject')).send_keys('''[{{ .Status | toUpper }}] {{ .GroupLabels.alertname }} alerts!''')
        webWaitEle(self, (
            By.ID, 'EmailTemplate')).send_keys(alertChannelTempStr)

        webWaitEle(self, (
            By.NAME, 'testEmailBtn')).click()
        util.getRequsetInfo1(
            self, self.driver, apiDict['testAlertChannelEmail'], closeModal)
        sleep(1)

        webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        util.getRequsetInfo1(
            self, self.driver, apiDict['createAlertChannel'], closeModal)
        sleep(2)

        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
            By.NAME, 'alertChannelOpBox')))
        opBoxs = self.driver.find_elements(
            By.NAME, 'alertChannelOpBox')
        if len(opBoxs) > 0:
            curOpBox = opBoxs[-1]

            WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
                By.NAME, 'alertChannelStatusBtn')))
            statusBtn = curOpBox.find_element(
                By.NAME, 'alertChannelStatusBtn')
            if statusBtn:
                statusBtn.click()
                sleep(1)
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.alertChannelStatusPopconfirm  button:nth-child(2)')).click()
                sleep(1)
                util.getRequsetInfo1(
                    self, self.driver, apiDict['updateAlertChannel'], closeModal)
                sleep(1)
                statusBtn.click()
                sleep(1)
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.alertChannelStatusPopconfirm  button:nth-child(2)')).click()
                sleep(1)
                util.getRequsetInfo1(
                    self, self.driver, apiDict['updateAlertChannel'], closeModal)
                sleep(1)
            deleteBtn = curOpBox.find_element(
                By.NAME, 'alertChannelDeleteBtn')
            if deleteBtn:
                deleteBtn.click()
                sleep(1)
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.alertChannelDeletePopconfirm  button:nth-child(2)')).click()
                sleep(1)
                util.getRequsetInfo1(
                    self, self.driver, apiDict['deleteAlertChannel'], closeModal)

        sleep(3)
        self.driver.quit()


if __name__ == '__main__':
    case = TestAlertChannel()
    case.test()
