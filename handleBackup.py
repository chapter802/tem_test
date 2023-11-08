# 执行备份恢复
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

from configParams import apiDict, backupDestination, backupAK, backupSK, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr, shortCutDateIDs, shortCutName, takeoverClusterHost, takeoverClusterPort, hostUserName, hostPwd, tiupPath, rangeStepArr, logLevelArr

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

# 测试用例中的接口
apiKeyArr = ['queryBackupTaskList', 'queryBackupTopSummary',
             'deleteBackupTask', 'backupCluster', 'restoreCluster', 'stopBackupTask', 'detectRestoreCluster', 'queryRestoreBackupList',
             'queryBackupPoliciesList', 'deleteBackupPolicy', 'createBackupPolicy', 'updateBackupPolicy', 'queryBackupPolicyDetail']


class Test(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
        # self.driver.maximize_window()
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

        # 返回集群列表
        def backToClusterList():
          sleep(2)
          webWaitEle(self, (By.NAME, 'menu.cluster')).click()
          for api in mainPageApiArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)
          sleep(2)
          js = "var q=document.documentElement.scrollTop=0"  # 滑动到顶部
          self.driver.execute_script(js)
          sleep(2)
        
        # self.driver.get('http://172.16.6.62:8080/login')
        self.driver.get('http://localhost:8050/login')

        mainWindowHanle = self.driver.current_window_handle

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)
        
        # 备份恢复
        webWaitEle(self, (By.NAME, 'menu.backup')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTaskList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTopSummary'], closeModal)
     
        # 手动备份
        webWaitEle(self, (By.NAME, 'manualBackupBtn')).click()
        webWaitEle(self, (By.NAME, 'backupModalClusterSelect')).click()
        clusterEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalClusterSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(clusterEles) > 0:
            random.choice(clusterEles).click()
        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_backup' + randomStr)
        webWaitEle(self, (By.ID, 'Destination')).send_keys(backupDestination.format(
            randomStr))
        webWaitEle(self, (By.ID, 'AccessKeyID')).send_keys(backupAK)
        webWaitEle(self, (By.ID, 'SecretAccessKey')).send_keys(backupSK)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['backupCluster'], closeModal)
        # 等待十秒备份
        sleep(10)
        
        # 跳转到集群管理页面
        backToClusterList()
        
        # 创建集群
        testClusterName = 'selenium_test_' + randomStr
        webWaitEle(self, (By.NAME, 'addClusterBtn')).click()
        clusterAliasEle = webWaitEle(self, (By.ID, 'Alias'))
        if clusterAliasEle:
            sleep(2)
            for api in addClusterApiArr:
                util.getRequsetInfo(
                    self, self.driver, apiDict[api], closeModal)
        clusterAliasEle.send_keys(testClusterName)
        webWaitEle(self, (By.ID, 'Password')).send_keys('tem')
        webWaitEle(self, (By.NAME, 'clusterVersionSelect')).click()
        sleep(1)
        clusterVersionOptions = webWaitEle(self, (By.CLASS_NAME, 'clusterVersionSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        randomClusterVersionOption = random.choice(clusterVersionOptions)
        randomClusterVersionOption.click()
        sleep(1)
        webWaitEle(self, (By.NAME, 'clusterArchSelect')).click()
        sleep(1)
        clusterArchOptions = webWaitEle(self, (By.CLASS_NAME, 'clusterArchSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        randomClusterArchOption = random.choice(clusterArchOptions)
        randomClusterArchOption.click()
        sleep(1)

        clusterModelEle = webWaitEle(self, (By.ID, 'Model'))
        shareClusterModelEle = clusterModelEle.find_element(
            By.CSS_SELECTOR, 'label.ant-radio-button-wrapper:nth-child(2)')
        shareClusterModelEle.click()
        clusterCollapseHeaders = self.driver.find_elements(
            By.CLASS_NAME, 'ant-collapse-header')
        for clusterCollapseHeader in clusterCollapseHeaders:
            if clusterCollapseHeader.get_attribute('aria-expanded') == 'false':
                clusterCollapseHeader.click()
                sleep(1)

        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)
        sleep(3)
        # 选择规模信息
        clusterSizeEle = webWaitEle(self, (By.ID, 'clusterSizeInfo'))
        deleteSizeInfoBtns = clusterSizeEle.find_elements(
            By.NAME, 'deleteSizeInfoBtn')
        for deleteSizeInfoBtn in deleteSizeInfoBtns:
            deleteSizeInfoBtn.click()
            sleep(1)

        sleep(1)
         # 选定指定IP
        clusterIPSelectEles = clusterSizeEle.find_elements(
            By.NAME, 'clusterIPSelect')
        isTargetIP = True
        for index, clusterIPSelectEle in enumerate(clusterIPSelectEles):  
            clusterIPSelectEle.click()
            sleep(1)
            clusterIPSelectDropdownEles = self.driver.find_elements(
                By.CLASS_NAME, 'clusterIPSelect')
            curOptions = clusterIPSelectDropdownEles[index].find_elements(
                By.CLASS_NAME, 'ant-select-item-option')            
            for curOption in curOptions:
                contentEle = curOption.find_element(
                    By.CLASS_NAME, 'ant-select-item-option-content')
                curText = util.getElementText(self, contentEle)
                if curText.find(hostIP) != -1:
                    print('clusterIPSelectEle---->',curOption)
                    curOption.click()
                    sleep(1)
                    break
                else:
                  clusterIPSelectEle.click()
                  isTargetIP = False
                  break
                 
            sleep(1)
        if isTargetIP:
          js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
          self.driver.execute_script(js)
          sleep(3)

          webWaitEle(self, (By.NAME, 'previewClusterBtn')).click()

          tableHeaderEle = webWaitEle(
              self, (By.CLASS_NAME, 'ant-table-thead'))
          
        
          
          if isElementWaitExist(self, (By.CLASS_NAME, 'ant-table-thead')):
              js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
              self.driver.execute_script(js)
              sleep(3)
              webWaitEle(self, (By.NAME, 'createClusterBtn')).click()
              sleep(30)
              util.getRequsetInfo(
                  self, self.driver, apiDict['clusterAdd'], closeModal)
              sleep(5)
              
              # webWaitEle(self, (By.NAME, 'menu.cluster')).click()
              # sleep(2)
              # js = "var q=document.documentElement.scrollTop=0"  # 滑动到顶部
              # self.driver.execute_script(js)
              # sleep(2)
          else: 
             backToClusterList()
        else:
          backToClusterList()
          pass
              
            
        # 手动恢复集群
        # 跳转到备份恢复页面
        webWaitEle(self, (By.NAME, 'menu.backup')).click()
        sleep(1)
        
        # 手动恢复
        webWaitEle(self, (By.NAME, 'manualRecoveryBtn')).click()

        def selectBackupRecoveryCluster(self):
            webWaitEle(self, (By.NAME, 'backupModalClusterSelect')).click()
            clusterEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalClusterSelect')).find_elements(
                By.CLASS_NAME, 'ant-select-item-option')
            if len(clusterEles) > 0:
                for clusterEle in clusterEles:
                    clusterEle.click()
                    webWaitEle(
                        self, (By.NAME, 'backupModalNameSelect')).click()
                    backupNameEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalNameSelect')).find_elements(
                        By.CLASS_NAME, 'ant-select-item-option')
                    print(len(backupNameEles))
                    if len(backupNameEles) > 0:
                        random.choice(backupNameEles).click()
                        break
                    else:
                        webWaitEle(
                            self, (By.NAME, 'backupModalClusterSelect')).click()
                        continue

        selectBackupRecoveryCluster(self)
        webWaitEle(self, (By.NAME, 'backupModalTargetClusterSelect')).click()
        tagetClusterEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalTargetClusterSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(tagetClusterEles) > 0:
            random.choice(tagetClusterEles).click()
            webWaitEle(self, (By.NAME, 'backupModalTestBtn')).click()
            util.getRequsetInfo(
                self, self.driver, apiDict['detectRestoreCluster'], closeModal)
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            util.getRequsetInfo(
                self, self.driver, apiDict['restoreCluster'], closeModal)
        else:
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-default').click()
            
         # 管理备份策略
        webWaitEle(self, (By.NAME, 'policyBtn')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupPoliciesList'], closeModal)
        # 新建备份策略
        webWaitEle(self, (By.NAME, 'createBackupPolicyBtn')).click()
        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_policy' + randomStr)
        webWaitEle(self, (By.ID, 'Destination')).send_keys(
            backupDestination.format(randomStr))
        webWaitEle(self, (By.ID, 'AccessKeyID')).send_keys(backupAK)
        webWaitEle(self, (By.ID, 'SecretAccessKey')).send_keys(backupSK)
        webWaitEle(self, (By.NAME, 'backupModalClusterIDsSelect')).click()
        applyClusterEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalClusterIDsSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(applyClusterEles) > 0:
            random.choice(applyClusterEles).click()
        else:
            pass

        backupPolicyWeekEle = webWaitEle(self, (By.ID, 'week'))
        if backupPolicyWeekEle:
            randomDays = random.sample(range(0, 7), random.randint(1, 7))
            weekdayEles = backupPolicyWeekEle.find_elements(
                By.CLASS_NAME, 'ant-checkbox-wrapper')
            for day in randomDays:
                weekdayEles[day-1].click()
        else:
            pass

        selectTimePicker(self, 'backupPolicyModalTimepicker')
        webWaitEle(self, (By.ID, 'Retention')).send_keys(
            random.randint(1, 365))

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createBackupPolicy'], closeModal)

        # 编辑备份策略
        webWaitEle(self, (By.NAME, 'backupPolicyEditBtn'))
        editBtns = self.driver.find_elements(
            By.NAME, 'backupPolicyEditBtn')
        if len(editBtns) > 0:
            lastEditBtn = editBtns[-1]
            lastEditBtn.click()
            policyNameEle = webWaitEle(self, (By.ID, 'Name'))
            util.clearInput(policyNameEle)
            policyNameEle.send_keys('selenium_policy' + randomStr + '_edit')
            backupDestinationEle = webWaitEle(self, (By.ID, 'Destination'))
            util.clearInput(backupDestinationEle)
            backupDestinationEle.send_keys(backupDestination.format(randomStr))

            backupPolicyWeekEle = webWaitEle(self, (By.ID, 'week'))
            if backupPolicyWeekEle:
                randomDays = random.sample(range(0, 7), random.randint(1, 7))
                weekdayEles = backupPolicyWeekEle.find_elements(
                    By.CLASS_NAME, 'ant-checkbox-wrapper')
                for day in randomDays:
                    weekdayEles[day-1].click()
            else:
                pass
            selectTimePicker(self, 'backupPolicyModalTimepicker')
            webWaitEle(self, (By.ID, 'Retention')).send_keys(
                random.randint(1, 365))

            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['updateBackupPolicy'], closeModal)

        else:
            pass

        sleep(3)

        # 删除备份策略
        webWaitEle(self, (By.NAME, 'backupPolicyDeleteBtn'))
        deleteBtns = self.driver.find_elements(
            By.NAME, 'backupPolicyDeleteBtn')
        if len(deleteBtns) > 0:
            lastDeleteBtn = deleteBtns[-1]
            lastDeleteBtn.click()

            confirmTagetVal = webWaitEle(
                self, (By.ID, 'PolicyName')).get_attribute('data-tval')
            webWaitEle(self, (By.ID, 'PolicyName')).send_keys(confirmTagetVal)

            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-danger').click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['deleteBackupPolicy'], closeModal)

        # 删除创建的集群 
        # 跳转到集群管理页面
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(2)
        
        try:
          testClusterEle = webWaitEle(
            self, (By.XPATH, "//*[contains(text(), '%s')]" % testClusterName))
          parentEle = testClusterEle.find_element(By.XPATH, '../../../..')
          parentEle.find_element(By.CLASS_NAME, 'destroyBtn').click()
          
          confirmTagetVal = webWaitEle(
                  self, (By.ID, 'Alias')).get_attribute('data-tval')
          webWaitEle(self, (By.ID, 'Alias')).send_keys(confirmTagetVal)
          webWaitEle(self, (By.CLASS_NAME, 'confirmDeleteClusterModal')).find_element(
              By.CLASS_NAME, 'ant-btn-danger').click()
          util.getRequsetInfo(
              self, self.driver, apiDict['destroyCluster'], closeModal)
          sleep(1)
        except:
          pass
        
        # 退出登录
        webWaitEle(self, (By.CLASS_NAME, 'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()

