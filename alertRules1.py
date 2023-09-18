from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import random
from util import util

from configParams import alertLevels, alertTypes, opArr, alertFrequencyUnits, apiDict

randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryAlertRuleList', 'createAlertRule',
             'updateAlertRule', 'switchAlertRuleStatus', 'deleteAlertRule', 'queryAlertRuleIndicators']


class TestAlertRules(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()

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

        self.driver.get('http://172.16.6.62:8080/login')
        sleep(1)
        self.driver.find_element(
            By.ID, 'userID').send_keys('selenium_test1')
        sleep(1)
        self.driver.find_element(By.ID, 'password').send_keys('123456')
        sleep(1)
        self.driver.find_element(By.ID, 'login').click()
        sleep(4)
        self.driver.find_element(By.NAME, 'menu.alert').click()
        sleep(1)
        self.driver.find_element(By.NAME, 'menu.alert.rules').click()
        sleep(3)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryAlertRuleIndicators'], closeModal)

        # 查询告警规则
        for x in alertLevels:
            self.driver.find_element(
                By.NAME, 'alertRulesLevelSelect').click()
            sleep(1)
            self.driver.find_element(By.NAME, x).click()
            self.driver.find_element(
                By.NAME, 'alertRulesSearchBtn').click()
            util.getRequsetInfo1(
                self, self.driver, apiDict['queryAlertRuleList'], closeModal)
            sleep(2)

            for y in alertTypes:
                self.driver.find_element(
                    By.NAME, 'alertRulesTypeSelect').click()
                sleep(1)
                self.driver.find_element(By.NAME, y).click()
                sleep(1)
                self.driver.find_element(
                    By.NAME, 'alertRulesSearchBtn').click()
                util.getRequsetInfo1(
                    self, self.driver, apiDict['queryAlertRuleList'], closeModal)
                sleep(2)

        # 新增告警规则
        self.driver.find_element(
            By.NAME, 'alertRulesAddBtn').click()
        sleep(2)
        randomStr = util.get_random_string(6)
        self.driver.find_element(
            By.ID, 'Name').send_keys('selenium_test_' + randomStr)
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesApplyType').click()
        sleep(1)
        applyTypes = self.driver.find_elements(
            By.NAME, 'modalApplyType')
        randomApplyType = random.choice(applyTypes)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomApplyType)
        randomApplyType.click()
        sleep(1)
        self.driver.find_element(
            By.ID, 'ApplyInstance').send_keys(util.generateIpAddress())
        sleep(1)
        self.driver.find_element(
            By.ID, 'Enabled').click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesIndicator').click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'indicators_0').click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesOpSelect_0').click()
        sleep(1)
        randomOp = random.choice(opArr)
        self.driver.find_element(By.NAME, randomOp).click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesThreshold_0').send_keys(random.randint(1, 100))
        sleep(1)
        self.driver.find_element(
            By.NAME, 'Duration_0').send_keys(random.randint(1, 100))
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesLevelSelect_0').click()
        sleep(1)
        modalAlertLevels = self.driver.find_elements(
            By.NAME, 'modalAlertRuleLevel_0')
        randomModalLevel = random.choice(modalAlertLevels)
        randomModalLevel.click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesFrequencyNum').send_keys(random.randint(1, 100))
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesFrequencyUnit').click()
        sleep(1)
        randomUnit = random.choice(alertFrequencyUnits)
        self.driver.find_element(
            By.NAME, randomUnit).click()
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesTimesThreshold').send_keys(random.randint(1, 100))
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesRetentionNum').send_keys(random.randint(1, 100))
        sleep(1)
        self.driver.find_element(
            By.NAME, 'alertRulesRetentionUnit').click()
        sleep(1)
        randomUnit1 = random.choice(alertFrequencyUnits)
        self.driver.find_element(
            By.NAME, 'RUnit_' + randomUnit1).click()
        sleep(1)

        self.driver.find_element(
            By.CLASS_NAME, 'ant-modal-footer').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['createAlertRule'], closeModal)
        sleep(2)

        # 修改告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)

        alertRulesUpdateBtns = self.driver.find_elements(
            By.NAME, 'alertRulesUpdateBtn')
        if len(alertRulesUpdateBtns) > 0:
            firstUpdateBtn = alertRulesUpdateBtns[0]
            firstUpdateBtn.click()
            sleep(2)

            randomStr = util.get_random_string(4)
            nameInput = self.driver.find_element(By.NAME, 'modalAlertRuleName')
            util.clearInput(nameInput)
            nameInput.send_keys('selenium_test_' + randomStr)
            self.driver.find_element(
                By.NAME, 'alertRulesApplyType').click()
            sleep(1)
            applyTypes = self.driver.find_elements(
                By.NAME, 'modalApplyType')
            randomApplyType = random.choice(applyTypes)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomApplyType)
            randomApplyType.click()
            applyInstanceInput = self.driver.find_element(
                By.ID, 'ApplyInstance')
            util.clearInput(applyInstanceInput)
            applyInstanceInput.send_keys(util.generateIpAddress())
            self.driver.find_element(
                By.ID, 'Enabled').click()
            self.driver.find_element(
                By.NAME, 'alertRulesIndicator').click()
            sleep(1)
            self.driver.find_element(
                By.NAME, 'indicators_0').click()
            self.driver.find_element(
                By.NAME, 'alertRulesOpSelect_0').click()
            randomOp = random.choice(opArr)
            self.driver.find_element(By.NAME, randomOp).click()
            alertRulesThresholdInput = self.driver.find_element(
                By.NAME, 'alertRulesThreshold_0')
            util.clearInput(alertRulesThresholdInput)
            alertRulesThresholdInput.send_keys(random.randint(1, 100))
            durationInput = self.driver.find_element(
                By.NAME, 'Duration_0')
            util.clearInput(durationInput)
            durationInput.send_keys(random.randint(1, 100))
            self.driver.find_element(
                By.NAME, 'alertRulesLevelSelect_0').click()
            sleep(1)
            modalAlertLevels = self.driver.find_elements(
                By.NAME, 'modalAlertRuleLevel_0')
            randomModalLevel = random.choice(modalAlertLevels)
            randomModalLevel.click()
            alertRulesFrequencyNumInput = self.driver.find_element(
                By.NAME, 'alertRulesFrequencyNum')
            util.clearInput(alertRulesFrequencyNumInput)
            alertRulesFrequencyNumInput.send_keys(random.randint(1, 100))
            self.driver.find_element(
                By.NAME, 'alertRulesFrequencyUnit').click()
            sleep(1)
            randomUnit = random.choice(alertFrequencyUnits)
            self.driver.find_element(
                By.NAME, randomUnit).click()
            alertRulesTimesThresholdInput = self.driver.find_element(
                By.NAME, 'alertRulesTimesThreshold')
            util.clearInput(alertRulesTimesThresholdInput)
            alertRulesTimesThresholdInput.send_keys(random.randint(1, 1000))
            alertRulesRetentionNumInput = self.driver.find_element(
                By.NAME, 'alertRulesRetentionNum')
            util.clearInput(alertRulesRetentionNumInput)
            alertRulesRetentionNumInput.send_keys(random.randint(1, 100))
            self.driver.find_element(
                By.NAME, 'alertRulesRetentionUnit').click()
            sleep(1)
            randomUnit1 = random.choice(alertFrequencyUnits)
            self.driver.find_element(
                By.NAME, 'RUnit_' + randomUnit1).click()

            self.driver.find_element(
                By.CLASS_NAME, 'ant-modal-footer').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)

            util.getRequsetInfo1(
                self, self.driver, apiDict['updateAlertRule'], closeModal)

        # 启用停用告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)
        sleep(1)
        statusBtns = self.driver.find_elements(
            By.NAME, 'alertRulesStatusBtn')
        if len(statusBtns) > 0:
            statusBtns[0].click()
            sleep(1)
            self.driver.find_element(
                By.CLASS_NAME, 'ant-popover-buttons').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver,  apiDict['switchAlertRuleStatus'], closeModal)
            sleep(3)
            statusBtns[0].click()
            sleep(1)
            self.driver.find_element(
                By.CLASS_NAME, 'ant-popover-buttons').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['switchAlertRuleStatus'], closeModal)
            sleep(3)
        # 删除告警规则
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)
        sleep(1)

        deleteBtns = self.driver.find_elements(
            By.NAME, 'alertRuleDeleteBtn')
        if len(deleteBtns) > 0:
            deleteBtns[0].click()
            sleep(1)
            self.driver.find_elements(
                By.CLASS_NAME, 'ant-popover-buttons')[1].find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteAlertRule'], closeModal)
        sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    case = TestAlertRules()
    case.test()
