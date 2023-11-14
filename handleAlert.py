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

from configParams import apiDict, testAlertRuleTempName, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr, shortCutDateIDs, shortCutName, takeoverClusterHost, takeoverClusterPort, hostUserName, hostPwd, tiupPath, rangeStepArr, logLevelArr

randomStr = util.get_random_string(6)


# 集群管理测试用例中的接口
clustersApiKeyArr = ['clusterList', 'clusterTops', 'clusterTopAlert', 'clusterPerfSummary', 'clusterAlertSummary', 'queryClusterMonitorInfo', 'queryHostOption', 'queryParamTemplateList',
                     'queryParamTemplateParams', 'queryHostList', 'queryParamTemplateDetail', 'clusterAdd', 'takeoverRemoteClusterList', 'takeoverRemoteDetail', 'takeoverCluster',]
# 集群管理 - 单个集群 测试用例中的接口
clusterApiKeyArr = ['clusterDetail', 'clusterInstance', 'clusterAlertSummary', 'queryClusterMonitorInfo', 'queryInpecReportList', 'queryClusterInspecReportDetail', 'deleteClusterInspecReport', 'queryClusterTopSqlList', 'queryClusterSlowQueryList', 'queryClusterDiagnoseReportList', 'createClusterDiagnoseReport',
                    'queryClusterDiagnoseReportStatus', 'queryClusterLogSearchTopology', 'queryClusterLogSearchTaskID', 'queryClusterLogSearchTaskList', 'queryClusterLogSearchList', 'queryBackupTaskList',  'queryBackupPolicy', 'updateBackupPolicy', 'detectRestoreCluster', 'clusterParamList', 'querySQLEditorMeta', 'querySQLEditorStatementHistory']

# 集群管理列表页请求的接口
mainPageApiArr = ['clusterList', 'clusterTops', 'clusterTopAlert',
                  'clusterPerfSummary', 'clusterAlertSummary', 'queryClusterMonitorInfo']
# 打开创建集群页面请求的接口
addClusterApiArr = ['queryHostOption', 'queryParamTemplateList',
                    'queryParamTemplateParams', 'queryHostList', 'queryParamTemplateDetail']
# 集群概览页请求的接口
clusterOverviewApiKeyArr = ['clusterDetail', 'clusterInstance',
                            'clusterAlertSummary', 'queryClusterMonitorInfo']
# 集群拓扑页请求的接口
clusterTopologyApiKeyArr = ['clusterDetail',
                            'clusterInstance', 'queryHostOption', 'queryHostList']


class Test(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test(self):
        # def autoPage(self):
        #     nextPageEl = self.driver.find_element(
        #         By.CLASS_NAME, 'ant-table-pagination').find_element(By.CLASS_NAME, 'ant-pagination-next')
        #     a = nextPageEl.get_attribute('aria-disabled')
        #     if a == 'false':
        #         nextPageEl.click()
        #         sleep(2)

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

        def isElementWaitExist(self, locator):
            try:
                WebDriverWait(self.driver, 20, 0.5).until(
                    EC.visibility_of_element_located(locator))
                return True
            except:
                return False

        # def selectDate(self, cb=None):
        #     randomDate = random.choice(shortCutDateIDs)
        #     self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
        #     webWaitEle(self, (
        #         By.NAME, shortCutName.format(id=randomDate))).click()
        #     if cb:
        #         cb(self)

        def selectTimePicker(self, compName):
            datePicker = self.driver.find_element(By.NAME, compName)
            datePicker.click()
            parentEle = webWaitEle(self, (By.CLASS_NAME, compName))
            pickerContent = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-content')
            pickerCells = pickerContent.find_elements(
                By.CLASS_NAME, 'ant-picker-cell-inner')
            
            if len(pickerCells) > 0:  # 日期选择
              randomPickerCell = random.choice(pickerCells)
              self.driver.execute_script(
                  "arguments[0].scrollIntoView();", randomPickerCell)
              randomPickerCell.click()
            else:
              pass

            timePanel = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-time-panel')
            timeColums = timePanel.find_elements(
                By.CLASS_NAME, 'ant-picker-time-panel-column')
            hourCellBox = timeColums[0]
            hourCells = hourCellBox.find_elements(
                By.CLASS_NAME, 'ant-picker-time-panel-cell')
            randomHour = random.choice(hourCells)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomHour)
            randomHour.click()
            sleep(1)

            minuteCellBox = timeColums[1]
            minuteCells = minuteCellBox.find_elements(
                By.CLASS_NAME, 'ant-picker-time-panel-cell')
            randomMinute = random.choice(minuteCells)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomMinute)
            randomMinute.click()
            sleep(1)

            datePickerFooter = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-footer')
            datePickerFooter.find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)

        # self.driver.get('http://172.16.6.62:8080/login')
        self.driver.get('http://localhost:8050/login')

        mainWindowHanle = self.driver.current_window_handle

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
          
        # # 查询告警规则
        # for x in alertLevels:
        #     webWaitEle(self, (
        #         By.NAME, 'alertRulesLevelSelect')).click()
        #     webWaitEle(self, (By.NAME, x)).click()
        #     webWaitEle(self, (
        #         By.NAME, 'alertRulesSearchBtn')).click()
        #     sleep(2)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryAlertRuleList'], closeModal)

        #     for y in alertTypes:
        #         webWaitEle(self, (
        #             By.NAME, 'alertRulesTypeSelect')).click()

        #         webWaitEle(self, (By.NAME, y)).click()
        #         webWaitEle(self, (
        #             By.NAME, 'alertRulesSearchBtn')).click()
        #         sleep(2)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['queryAlertRuleList'], closeModal)
        
        sleep(2)
        
        # 选中 TiDB_monitor_keep_alive_copy 规则修改频率
        webWaitEle(self, (By.ID, 'Name')).send_keys(testAlertRuleTempName)
        webWaitEle(self, (
            By.NAME, 'alertRulesSearchBtn')).click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAlertRuleList'], closeModal)
        sleep(2)
        
        #找到 TiDB_monitor_keep_alive_copy 规则
        testRuleEle = webWaitEle(
                self, (By.XPATH, "//*[contains(text(), '%s')]" % testAlertRuleTempName))
        # testRuleEle = webWaitEle(
        #         self, (By.XPATH, "//*[contains(text(), 'TiDB_monitor_keep_alive_copy')]"))
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
        
        if len(relateARItems) > 0:
            js = "var q=document.getElementsByClassName('relateAlertRuleDropdown')[0].getElementsByClassName('rc-virtual-list-holder-inner')[0].scrollTop=10000"  # 滑动到底部
            self.driver.execute_script(js)
            for option in relateARItems:
                if testAlertRuleName in option.get_attribute('title'):
                    self.driver.execute_script("arguments[0].scrollIntoView();", option)
                    sleep(1)
                    option.click()
                    break

        randomStr = util.get_random_string(6)
        webWaitEle(self, (
            By.ID, 'Name')).send_keys(testAlertRuleName)
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
        webWaitEle(self, (By.CLASS_NAME, 'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()

