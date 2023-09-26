from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import random
from util import util

from configParams import alertLevels, alertTypes, opArr, alertFrequencyUnits, apiDict

driver = webdriver.Chrome()
driver.implicitly_wait(10)

randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryAlertRuleList', 'createAlertRule',
             'updateAlertRule', 'switchAlertRuleStatus', 'deleteAlertRule', 'queryAlertRuleIndicators']


class TestAlertRules(object):
    def __init__(self):
        self.driver = driver
        self.logger = util.get_logger()
        self.driver.maximize_window()

    def test(self):

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

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))

        self.driver.get('http://172.16.6.62:8080/login')
        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        webWaitEle(self, (By.NAME, 'menu.alert')).click()
        webWaitEle(self, (By.NAME, 'menu.alert.rules')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryAlertRuleIndicators'], closeModal)

        # 查询告警规则
        for x in alertLevels:
            webWaitEle(self, (
                By.NAME, 'alertRulesLevelSelect')).click()
            webWaitEle(self, (By.NAME, x)).click()
            webWaitEle(self, (
                By.NAME, 'alertRulesSearchBtn')).click()
            sleep(2)
            util.getRequsetInfo1(
                self, self.driver, apiDict['queryAlertRuleList'], closeModal)

            for y in alertTypes:
                webWaitEle(self, (
                    By.NAME, 'alertRulesTypeSelect')).click()

                webWaitEle(self, (By.NAME, y)).click()
                webWaitEle(self, (
                    By.NAME, 'alertRulesSearchBtn')).click()
                sleep(2)
                util.getRequsetInfo1(
                    self, self.driver, apiDict['queryAlertRuleList'], closeModal)

        # 新增告警规则
        webWaitEle(self, (
            By.NAME, 'alertRulesAddBtn')).click()
        sleep(1)
        randomStr = util.get_random_string(6)
        webWaitEle(self, (
            By.NAME, 'ruleModalName')).send_keys('selenium_test_' + randomStr)
        sleep(1)
        webWaitEle(self, (
            By.NAME, 'alertRulesApplyType')).click()
        applyTypes = self.driver.find_elements(
            By.NAME, 'modalApplyType')
        randomApplyType = random.choice(applyTypes)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomApplyType)
        sleep(1)
        randomApplyType.click()
        webWaitEle(self, (
            By.ID, 'ApplyInstance')).send_keys(util.generateIpAddress())
        webWaitEle(self, (
            By.ID, 'Enabled')).click()
        webWaitEle(self, (
            By.NAME, 'alertRulesIndicator')).click()
        webWaitEle(self, (
            By.NAME, 'indicators_0')).click()
        webWaitEle(self, (
            By.NAME, 'alertRulesOpSelect_0')).click()
        randomOp = random.choice(opArr)
        webWaitEle(self, (By.NAME, randomOp)).click()
        webWaitEle(self, (
            By.NAME, 'alertRulesThreshold_0')).send_keys(random.randint(1, 100))
        webWaitEle(self, (
            By.NAME, 'Duration_0')).send_keys(random.randint(1, 100))
        webWaitEle(self, (
            By.NAME, 'alertRulesLevelSelect_0')).click()
        modalAlertLevels = self.driver.find_elements(
            By.NAME, 'modalAlertRuleLevel_0')
        randomModalLevel = random.choice(modalAlertLevels)
        randomModalLevel.click()
        webWaitEle(self, (
            By.NAME, 'alertRulesFrequencyNum')).send_keys(random.randint(1, 100))
        webWaitEle(self, (
            By.NAME, 'alertRulesFrequencyUnit')).click()
        randomUnit = random.choice(alertFrequencyUnits)
        webWaitEle(self, (
            By.NAME, randomUnit)).click()
        sleep(1)
        webWaitEle(self, (
            By.NAME, 'alertRulesTimesThreshold')).send_keys(random.randint(1, 100))
        webWaitEle(self, (
            By.NAME, 'alertRulesRetentionNum')).send_keys(random.randint(1, 100))
        webWaitEle(self, (
            By.NAME, 'alertRulesRetentionUnit')).click()
        randomUnit1 = random.choice(alertFrequencyUnits)
        webWaitEle(self, (
            By.NAME, 'RUnit_' + randomUnit1)).click()

        webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        util.getRequsetInfo1(
            self, self.driver, apiDict['createAlertRule'], closeModal)
        sleep(2)
        # 修改告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)
        sleep(2)

        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
            By.NAME, 'alertRulesUpdateBtn')))
        alertRulesUpdateBtn = webWaitEle(self, (
            By.NAME, 'alertRulesUpdateBtn'))
        if alertRulesUpdateBtn:
            firstUpdateBtn = alertRulesUpdateBtn
            firstUpdateBtn.click()

            randomStr = util.get_random_string(4)
            nameInput = webWaitEle(self, (By.NAME, 'ruleModalName'))
            util.clearInput(nameInput)
            nameInput.send_keys('selenium_test_' + randomStr)
            webWaitEle(self, (
                By.NAME, 'alertRulesApplyType')).click()
            applyTypes = self.driver.find_elements(
                By.NAME, 'modalApplyType')
            randomApplyType = random.choice(applyTypes)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomApplyType)
            sleep(1)
            randomApplyType.click()
            applyInstanceInput = webWaitEle(self, (
                By.ID, 'ApplyInstance'))
            util.clearInput(applyInstanceInput)
            applyInstanceInput.send_keys(util.generateIpAddress())
            webWaitEle(self, (
                By.ID, 'Enabled')).click()
            webWaitEle(self, (
                By.NAME, 'alertRulesIndicator')).click()
            webWaitEle(self, (
                By.NAME, 'indicators_0')).click()
            webWaitEle(self, (
                By.NAME, 'alertRulesOpSelect_0')).click()
            randomOp = random.choice(opArr)
            webWaitEle(self, (By.NAME, randomOp)).click()
            alertRulesThresholdInput = webWaitEle(self, (
                By.NAME, 'alertRulesThreshold_0'))
            util.clearInput(alertRulesThresholdInput)
            alertRulesThresholdInput.send_keys(random.randint(1, 100))
            durationInput = webWaitEle(self, (
                By.NAME, 'Duration_0'))
            util.clearInput(durationInput)
            durationInput.send_keys(random.randint(1, 100))
            webWaitEle(self, (
                By.NAME, 'alertRulesLevelSelect_0')).click()
            modalAlertLevels = self.driver.find_elements(
                By.NAME, 'modalAlertRuleLevel_0')
            randomModalLevel = random.choice(modalAlertLevels)
            randomModalLevel.click()
            alertRulesFrequencyNumInput = webWaitEle(self, (
                By.NAME, 'alertRulesFrequencyNum'))
            util.clearInput(alertRulesFrequencyNumInput)
            alertRulesFrequencyNumInput.send_keys(random.randint(1, 100))
            webWaitEle(self, (
                By.NAME, 'alertRulesFrequencyUnit')).click()
            randomUnit = random.choice(alertFrequencyUnits)
            webWaitEle(self, (
                By.NAME, randomUnit)).click()
            alertRulesTimesThresholdInput = webWaitEle(self, (
                By.NAME, 'alertRulesTimesThreshold'))
            util.clearInput(alertRulesTimesThresholdInput)
            alertRulesTimesThresholdInput.send_keys(random.randint(1, 1000))
            alertRulesRetentionNumInput = webWaitEle(self, (
                By.NAME, 'alertRulesRetentionNum'))
            util.clearInput(alertRulesRetentionNumInput)
            alertRulesRetentionNumInput.send_keys(random.randint(1, 100))
            webWaitEle(self, (
                By.NAME, 'alertRulesRetentionUnit')).click()
            randomUnit1 = random.choice(alertFrequencyUnits)
            webWaitEle(self, (
                By.NAME, 'RUnit_' + randomUnit1)).click()

            webWaitEle(self, (
                By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            util.getRequsetInfo1(
                self, self.driver, apiDict['updateAlertRule'], closeModal)
            sleep(2)
        # 启用停用告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)
        sleep(2)
        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
            By.NAME, 'alertRulesStatusBtn')))
        statusBtn = webWaitEle(self, (
            By.NAME, 'alertRulesStatusBtn'))
        if statusBtn:
            statusBtn.click()
            # sleep(2)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo1(
                self, self.driver,  apiDict['switchAlertRuleStatus'], closeModal)
            sleep(2)
            statusBtn.click()
            # sleep(2)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo1(
                self, self.driver, apiDict['switchAlertRuleStatus'], closeModal)

        # 删除告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)
        sleep(2)

        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
            By.NAME, 'alertRuleDeleteBtn')))
        webWaitEle(self, (
            By.NAME, 'alertRuleDeleteBtn')).click()
        sleep(1)
        webWaitEle(self, (
            By.CSS_SELECTOR, 'div.alertRuleDeletePopconfirm button:nth-child(2)')).click()
        util.getRequsetInfo1(
            self, self.driver, apiDict['deleteAlertRule'], closeModal)
        sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    case = TestAlertRules()
    case.test()
