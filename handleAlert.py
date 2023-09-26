# 处理集群告警
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

from util import util

from configParams import testServer, apiDict, testAlertRuleTempName, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr, SMTPAddress, SMTPUsername, SMTPPassword, SMTPSender, SMTPSenderEmail, SMTPReceiverEmail

randomStr = util.get_random_string(6)


class Test(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

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

            try:
                cusModalCloseBtn = self.driver.find_element(
                    By.NAME, 'cancelBtn')
            except:
                cusModalCloseBtn = None

            if notiCLoseEle != None:
                notiCLoseEle.click()
            elif drawerCusCloseBtn != None:
                drawerCusCloseBtn.click()
            elif modalCloseBtn != None:
                modalCloseBtn.click()
            elif cusModalCloseBtn != None:
                cusModalCloseBtn.click()

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))

        self.driver.get(testServer)

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)

        #  告警管理
        webWaitEle(self, (By.NAME, 'menu.alert')).click()
        webWaitEle(self, (By.NAME, 'menu.alert.rules')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAlertRuleIndicators'], closeModal)

        # 查询告警规则
        for x in alertLevels:
            webWaitEle(self, (
                By.NAME, 'alertRulesLevelSelect')).click()
            webWaitEle(self, (By.NAME, x)).click()
            webWaitEle(self, (
                By.NAME, 'alertRulesSearchBtn')).click()
            sleep(2)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryAlertRuleList'], closeModal)

            for y in alertTypes:
                webWaitEle(self, (
                    By.NAME, 'alertRulesTypeSelect')).click()

                webWaitEle(self, (By.NAME, y)).click()
                webWaitEle(self, (
                    By.NAME, 'alertRulesSearchBtn')).click()
                sleep(2)
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryAlertRuleList'], closeModal)

        sleep(2)

        # 选中 TiDB_monitor_keep_alive_copy 规则修改频率
        webWaitEle(self, (
            By.NAME, 'alertRulesLevelSelect')).click()
        sleep(1)
        dropdownLevelEle = webWaitEle(
            self, (By.CLASS_NAME, 'alertRulesLevelSelect'))
        dropdownLevelEle.find_elements(
            By.CLASS_NAME, 'ant-select-item-option')[0].click()
        sleep(1)

        webWaitEle(self, (
            By.NAME, 'alertRulesTypeSelect')).click()
        sleep(1)
        dropdownTypeEle = webWaitEle(
            self, (By.CLASS_NAME, 'alertRulesTypeSelect'))
        dropdownTypeEle.find_elements(
            By.CLASS_NAME, 'ant-select-item-option')[0].click()
        sleep(1)

        webWaitEle(self, (By.ID, 'Name')).send_keys(testAlertRuleTempName)
        webWaitEle(self, (
            By.NAME, 'alertRulesSearchBtn')).click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAlertRuleList'], closeModal)
        sleep(2)

        # 找到 TiDB_monitor_keep_alive_copy 规则
        testRuleEle = webWaitEle(
            self, (By.XPATH, "//*[contains(text(), '%s')]" % testAlertRuleTempName))
        parentEle = testRuleEle.find_element(By.XPATH, '../../../..')
        parentEle.find_element(By.NAME, 'alertRulesUpdateBtn').click()

        # 修改告警频率
        tempRulesFrequencyUnitEle = webWaitEle(self, (
            By.NAME, 'alertRulesFrequencyNum'))
        util.clearInput(tempRulesFrequencyUnitEle)
        tempRulesFrequencyUnitEle.send_keys(1)
        webWaitEle(self, (
            By.NAME, 'alertRulesFrequencyUnit')).click()
        webWaitEle(self, (
            By.NAME, alertFrequencyUnits[0])).click()
        sleep(1)
        webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        util.getRequsetInfo(
            self, self.driver, apiDict['createAlertRule'], closeModal)
        sleep(2)

        # 新增告警规则
        webWaitEle(self, (
            By.NAME, 'alertRulesAddBtn')).click()
        sleep(1)
        randomStr = util.get_random_string(6)
        testAlertRuleName = 'selenium_test_' + randomStr
        webWaitEle(self, (
            By.NAME, 'ruleModalName')).send_keys(testAlertRuleName)
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
            By.ID, 'ApplyInstance')).send_keys(hostIP)
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
        util.getRequsetInfo(
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
            nameInput.send_keys(testAlertRuleName)
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
            applyInstanceInput.send_keys(hostIP)
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
            util.getRequsetInfo(
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
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo(
                self, self.driver,  apiDict['switchAlertRuleStatus'], closeModal)
            sleep(2)
            statusBtn.click()
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo(
                self, self.driver, apiDict['switchAlertRuleStatus'], closeModal)

        sleep(2)
        # 创建告警通道
        webWaitEle(self, (
            By.NAME, 'menu.alert.channel')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAlertChannelList'], closeModal)

        # 查询告警通道
        for x in alertChannelTypes:
            webWaitEle(self, (
                By.NAME, 'alertChannelTypeSelect')).click()
            sleep(1)
            typeDropdown = self.driver.find_element(
                By.CLASS_NAME, 'alertChannelTypeDropdown')
            typeDropdown.find_element(By.NAME, x).click()
            webWaitEle(self, (By.NAME, 'alertChannelSearchBtn')).click()
            util.getRequsetInfo(
                self, self.driver, apiDict['queryAlertChannelList'], closeModal)
            sleep(1)

            for y in alertChannelEnabled:
                webWaitEle(self, (
                    By.NAME, 'alertChannelEnabledSelect')).click()
                sleep(1)
                enabledDropdown = self.driver.find_element(
                    By.CLASS_NAME, 'alertChannelEnabledDropdown')
                enabledDropdown.find_element(By.NAME, y).click()
                webWaitEle(self, (By.NAME, 'alertChannelSearchBtn')).click()
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryAlertChannelList'], closeModal)
                sleep(1)

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

        addRuleNum = 0

        if len(relateARItems) > 0:
            # 滑动到底部
            js = "var q=document.getElementsByClassName('relateAlertRuleDropdown')[0].getElementsByClassName('rc-virtual-list-holder-inner')[0].scrollTop=10000"
            self.driver.execute_script(js)
            for option in relateARItems:
                if testAlertRuleName in option.get_attribute('title') or testAlertRuleTempName in option.get_attribute('title') and addRuleNum < 2:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", option)
                    sleep(1)
                    option.click()
                    addRuleNum += 1
                else:
                    pass

        randomStr = util.get_random_string(6)
        webWaitEle(self, (
            By.ID, 'Name')).send_keys(testAlertRuleName)
        webWaitEle(self, (
            By.ID, 'SMTPAddress')).send_keys(SMTPAddress)
        webWaitEle(self, (
            By.ID, 'SMTPUsername')).send_keys(SMTPUsername)
        webWaitEle(self, (
            By.ID, 'SMTPPassword')).send_keys(SMTPPassword)
        webWaitEle(self, (
            By.ID, 'Sender')).send_keys(SMTPSender)
        webWaitEle(self, (
            By.ID, 'EmailFrom')).send_keys(SMTPSenderEmail)
        webWaitEle(self, (
            By.ID, 'EmailTo')).send_keys(SMTPReceiverEmail)
        webWaitEle(self, (
            By.ID, 'EmailSubject')).send_keys('''[{{ .Status | toUpper }}] {{ .GroupLabels.alertname }} alerts!''')
        webWaitEle(self, (
            By.ID, 'EmailTemplate')).send_keys(alertChannelTempStr)

        webWaitEle(self, (
            By.NAME, 'testEmailBtn')).click()
        util.getRequsetInfo(
            self, self.driver, apiDict['testAlertChannelEmail'], closeModal)
        sleep(1)

        webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        util.getRequsetInfo(
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
                util.getRequsetInfo(
                    self, self.driver, apiDict['updateAlertChannel'], closeModal)
                sleep(1)
                statusBtn.click()
                sleep(1)
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.alertChannelStatusPopconfirm  button:nth-child(2)')).click()
                sleep(1)
                util.getRequsetInfo(
                    self, self.driver, apiDict['updateAlertChannel'], closeModal)
                sleep(1)

        # 退出登录
        webWaitEle(self, (By.CLASS_NAME,
                   'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()
