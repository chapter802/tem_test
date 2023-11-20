# 纳管已有集群
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
from configParams import testServer, apiDict, backupDestination, backupAK, backupSK, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr,  backupRateLimitArr, backupConcurrencyArr, backupLogFileArr, takeoverClusterHost, takeoverClusterPort, hostUserName, hostPwd, tiupPath, takeoverClusterPwd


# 集群管理列表页请求的接口
mainPageApiArr = ['clusterList', 'clusterTops', 'clusterTopAlert',
                  'clusterPerfSummary', 'clusterAlertSummary', 'queryClusterMonitorInfo']

# 集群概览页请求的接口
clusterOverviewApiKeyArr = ['clusterDetail', 'clusterInstance',
                            'clusterAlertSummary', 'queryClusterMonitorInfo']

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

        def isElementWaitExist(self, locator):
            try:
                WebDriverWait(self.driver, 20, 0.5).until(
                    EC.visibility_of_element_located(locator))
                return True
            except:
                return False

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
            
        # 备份填写高级选项
        def fillBackupAdvancedOptions(self):
            webWaitEle(self, (By.CLASS_NAME, 'ant-collapse-header')).click()
            sleep(1)
            randomRateLimit = random.choice(backupRateLimitArr)
            rateLimitEle = webWaitEle(self, (By.ID, 'RateLimit'))
            util.clearInput(rateLimitEle)
            rateLimitEle.send_keys(randomRateLimit)
            randomConcurrency = random.choice(backupConcurrencyArr)
            concurrencEle = webWaitEle(self, (By.ID, 'Concurrency'))
            util.clearInput(concurrencEle)
            concurrencEle.send_keys(
                randomConcurrency)
            randomLogFile = random.choice(backupLogFileArr)
            logFileEle = webWaitEle(self, (By.ID, 'LogFile'))
            util.clearInput(logFileEle)
            logFileEle.send_keys(randomLogFile)
            sleep(1)

        randomStr = util.get_random_string(6)
        
        self.driver.get(testServer)

        mainWindowHanle = self.driver.current_window_handle

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)
        
        #集群列表
        backToClusterList()
        
         # 纳管集群
        webWaitEle(self, (By.NAME, 'takeoverClusterBtn')).click()
        webWaitEle(self, (By.ID, 'Host')).send_keys(takeoverClusterHost)
        webWaitEle(self, (By.ID, 'Port')).send_keys(takeoverClusterPort)
        webWaitEle(self, (By.ID, 'User')).send_keys(hostUserName)
        webWaitEle(self, (By.ID, 'Password')).send_keys(takeoverClusterPwd)
        webWaitEle(self, (By.ID, 'TiUPHome')).send_keys(tiupPath)
        webWaitEle(self, (By.NAME, 'getTakeOverClusterListBtn')).click()
        sleep(10)
        util.getRequsetInfo(
            self, self.driver, apiDict['takeoverRemoteClusterList'], closeModal)
        
        webWaitEle(self, (By.NAME, 'confirmTakeoverBtn'))

        isExistCluster = isElementWaitExist(self, (By.CLASS_NAME, 'ant-table-row'))
        if isExistCluster == True:
            sleep(5)
            takeoverRows = self.driver.find_elements(
                By.CLASS_NAME, 'ant-table-row')
            lastTakeoverRow = takeoverRows[-1]
            nthchild3Cell = lastTakeoverRow.find_element(
                By.CSS_SELECTOR, 'td:nth-child(3)')
            takeoverClusterName = util.getElementText(self, nthchild3Cell)
            if takeoverClusterName != 'tem_metadb':
                try:
                    tableExpandEle = lastTakeoverRow.find_element(
                        By.CSS_SELECTOR, 'td:nth-child(2)').find_element(By.CLASS_NAME, 'ant-table-row-expand-icon')
                    if tableExpandEle.get_attribute('aria-expanded') == 'false':
                        tableExpandEle.click()
                        sleep(10)
                        util.getRequsetInfo(
                            self, self.driver, apiDict['takeoverRemoteDetail'], closeModal)
                        sleep(1)
                except:
                    pass

                try:
                    tableCheckWrapperEle = lastTakeoverRow.find_element(
                        By.CSS_SELECTOR, 'td:nth-child(1)').find_element(By.CLASS_NAME, 'ant-checkbox-wrapper')
                    tableCheckWrapperEle.click()
                except:
                    pass

                confirmTakeoverBtn = webWaitEle(
                    self, (By.NAME, 'confirmTakeoverBtn'))
                if confirmTakeoverBtn.get_attribute('disabled') == None:
                    confirmTakeoverBtn.click()
                    sleep(1)
                    # 默认为 root , 无需再次填写
                    # webWaitEle(self, (By.ID, 'UserID_' +
                    #            takeoverClusterName)).send_keys(hostUserName)
                  
                    webWaitEle(self,  (By.ID, 'Password_' +
                               takeoverClusterName)).send_keys(hostPwd)
                    webWaitEle(self, (By.NAME, 'modelSelect_' +
                               takeoverClusterName)).click()
                    sleep(1)
                    takeoverDropdownEle = webWaitEle(
                        self, (By.CLASS_NAME,  'modelSelect_' +
                               takeoverClusterName))
                    # 'ant-select-item-option'
                    takeoverDropdownOptions = takeoverDropdownEle.find_elements(
                        By.CLASS_NAME, 'ant-select-item-option')
                    if len(takeoverDropdownOptions) > 0:
                        for takeoverDropdownOption in takeoverDropdownOptions:
                            if takeoverDropdownOption.get_attribute('title') == '共享模式':
                                takeoverDropdownOption.click()
                                sleep(1)

                    webWaitEle(self, (By.CLASS_NAME, 'takeoverInputPwdModal')).find_element(
                        By.CLASS_NAME, 'ant-modal-footer').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
                    sleep(10)
                    util.getRequsetInfo(
                        self, self.driver, apiDict['takeoverCluster'], closeModal)
                    
                    # webWaitEle(self, (By.NAME, 'takeoverClusterBtn'))
                else:
                    cancelTakeoverBtn = webWaitEle(
                        self, (By.NAME, 'cancelTakeoverBtn'))
                    cancelTakeoverBtn.click()
        
        sleep(1)
        
        backToClusterList()
        
        try:
          takeoverEle = webWaitEle(
              self, (By.XPATH, "//*[contains(text(), '纳管中')]"))
          
          parentEle = takeoverEle.find_element(By.XPATH, '../../../..')
          targetNameCell = parentEle.find_elements(By.CLASS_NAME, 'ant-table-cell')[0].find_element(By.TAG_NAME, 'span')
          takeoverClusterName = targetNameCell.get_attribute('innerHTML')
        
          sleep(180)  #纳管等待 3 分钟
          self.driver.refresh()
          sleep(2)
          takeoverClusterEle = webWaitEle(
              self, (By.XPATH, "//*[contains(text(), '%s')]" % takeoverClusterName))
          targetClusterEle = takeoverClusterEle.find_element(By.XPATH, '..')
          # targetClusterEle.click()
        except:
          pass
        
        # 修改参数组模板
        # 待补充
        
        
        
        # 重启集群 
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if takeoverClusterName in activeClusterName:
                    parentEle = activeCluster.find_element(By.XPATH, '../..')
                    try:
                      parentEle.find_element(By.NAME, 'restartBtn').click()
                      sleep(1)
                      webWaitEle(self, (By.CLASS_NAME, 'clusterConfirmModal')).find_element(
                      By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
                      sleep(3)
                      util.getRequsetInfo(self, self.driver, apiDict['restartCluster'], closeModal)
                      break
                    except:
                      continue
        
        sleep(180) #重启等待 3 分钟
        self.driver.refresh()
        
        # 找到目标集群 - 进入集群概览
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if takeoverClusterName in activeClusterName:
                    activeCluster.click()
                    break
        else:
            # util.logger.debug('未找到对应的测试集群')
            sleep(5)
            self.driver.quit()
            
        # 单个集群 - 备份恢复
        webWaitEle(self, (By.NAME, 'menu.cluster.single.backup')).click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTaskList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupPolicy'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['clusterList'], closeModal)

        # 手动备份
        webWaitEle(self, (By.NAME, 'manualBackupBtn')).click()
        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_test_' + randomStr)
        webWaitEle(self, (By.ID, 'Destination')).send_keys(backupDestination.format(
            randomStr))
        webWaitEle(self, (By.ID, 'AccessKeyID')).send_keys(backupAK)
        webWaitEle(self, (By.ID, 'SecretAccessKey')).send_keys(backupSK)
        fillBackupAdvancedOptions(self)
        
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['backupCluster'], closeModal) 
        sleep(2)
        
        try:
           webWaitEle(self, (By.NAME, 'backupConfigBtn'))
        except:
           webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-default').click()
        sleep(1)
        
        # 备份设置
        webWaitEle(self, (By.NAME, 'backupConfigBtn')).click()
        webWaitEle(self, (By.NAME, 'brPolicySelect')).click()
        sleep(1)
        brPolicyOptions = webWaitEle(self, (By.CLASS_NAME, 'brPolicySelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(brPolicyOptions) > 0:
            randomBrPolicyOption = random.choice(brPolicyOptions)
            randomBrPolicyOption.click()
            sleep(1)
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            util.getRequsetInfo(
                self, self.driver, apiDict['updateBackupPolicy'], closeModal)
        else:
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-default').click()

        sleep(10)
        webWaitEle(self, (By.NAME, 'backupRecoveryBtn')).click()
        webWaitEle(self, (By.NAME, 'BRTaskIDSelect')).click()
        BRTaskIDOptions = webWaitEle(self, (By.CLASS_NAME, 'BRTaskIDSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(BRTaskIDOptions) > 0:
            randomBRTaskIDOption = random.choice(BRTaskIDOptions)
            randomBRTaskIDOption.click()
            sleep(1)
        else:
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-default').click()

        webWaitEle(self, (By.NAME, 'targetClusterIDSelect')).click()
        try:
            targetClusterIDOptions = webWaitEle(self, (By.CLASS_NAME, 'targetClusterIDSelect')).find_elements(
                By.CLASS_NAME, 'ant-select-item-option')
            if len(targetClusterIDOptions) > 0:
                randomTargetClusterIDOption = random.choice(
                    targetClusterIDOptions)
                randomTargetClusterIDOption.click()
                sleep(1)

                webWaitEle(self, (By.NAME, 'brTestClusterBtn')).click()
                sleep(1)
                util.getRequsetInfo(
                    self, self.driver, apiDict['detectRestoreCluster'], closeModal)
                sleep(1)
                webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                    By.CLASS_NAME, 'ant-btn-primary').click()
                sleep(1)
                util.getRequsetInfo(
                    self, self.driver, apiDict['restoreCluster'], closeModal)

            else:
                webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                    By.CLASS_NAME, 'ant-btn-default').click()
        except:
            pass
        sleep(1)      
        
        # 修改巡检策略
        # 滚动到页面顶部
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)       
    
        webWaitEle(self, (By.NAME, 'headSettingIcon')).click()
        sleep(1)
        webWaitEle(
            self, (By.CLASS_NAME, 'headerSettingDropdown')).find_element(By.NAME, 'menu.inspection').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryInspecPolicyList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryInspections'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['clusterList'], closeModal)
        self.driver.find_element(By.TAG_NAME, 'body').click()
        sleep(1)

        # 创建巡检策略
        webWaitEle(self, (By.NAME, 'addInspectionPolicyBtn')).click()
        webWaitEle(self, (By.ID, 'Alias')).send_keys(
            'selenium_test_' + randomStr)
        webWaitEle(self, (By.NAME, 'inspecPolicySwitch')).click()
        webWaitEle(self, (By.ID, 'Description')).send_keys(
            'selenium_Description_' + randomStr)

        inpecPolicyWeekEle = webWaitEle(self, (By.ID, 'FrequencyWeek'))
        if inpecPolicyWeekEle:
            randomDays = random.sample(range(0, 7), random.randint(1, 7))
            weekdayEles = inpecPolicyWeekEle.find_elements(
                By.CLASS_NAME, 'ant-checkbox-wrapper')
            for day in randomDays:
                weekdayEles[day-1].click()
        else:
            pass

        selectTimePicker(self, 'inspecPolicyModalTimepicker')

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createInspecPolicy'], closeModal)

        #  巡检策略详情
        inspecPolicyAliasBtns = self.driver.find_elements(
            By.NAME, 'inspecPolicyAliasBtn')
        randomPolicyAliasBtn = random.choice(inspecPolicyAliasBtns)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomPolicyAliasBtn)
        randomPolicyAliasBtn.click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryInspecPolicyDetail'], closeModal)
        webWaitEle(self, (By.CLASS_NAME, 'ant-drawer-close')).click()

        # 编辑巡检策略
        updateInspectionPolicyBtns = self.driver.find_elements(
            By.NAME, 'updateInspectionPolicyBtn')
        lastUpdateInspectionPolicyBtn = updateInspectionPolicyBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastUpdateInspectionPolicyBtn)
        sleep(1)
        lastUpdateInspectionPolicyBtn.click()
        sleep(1)
        inpspecModalAlias = webWaitEle(self, (By.ID, 'Alias'))
        util.clearInput(inpspecModalAlias)
        inpspecModalAlias.send_keys('selenium_test_' + randomStr)
        webWaitEle(self, (By.NAME, 'inspecPolicySwitch')).click()
        inpspecModalDesc = webWaitEle(self, (By.ID, 'Description'))
        util.clearInput(inpspecModalDesc)
        inpspecModalDesc.send_keys('selenium_Description_' + randomStr)

        inpecPolicyWeekEle = webWaitEle(self, (By.ID, 'FrequencyWeek'))
        if inpecPolicyWeekEle:
            randomDays = random.sample(range(0, 7), random.randint(1, 7))
            weekdayEles = inpecPolicyWeekEle.find_elements(
                By.CLASS_NAME, 'ant-checkbox-wrapper')
            for day in randomDays:
                weekdayEles[day-1].click()
        else:
            pass

        selectTimePicker(self, 'inspecPolicyModalTimepicker')

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['updateInspecPolicy'], closeModal)

        # 应用集群
        applyClusterBtns = self.driver.find_elements(
            By.NAME, 'applyClusterBtn')

        lastApplyClusterBtn = applyClusterBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastApplyClusterBtn)
        sleep(1)
        lastApplyClusterBtn.click()
        
        webWaitEle(self, (By.NAME, 'inspecApplyClusterSelect')).click()
        inspecApplyClusterSelectOptions = webWaitEle(
            self, (By.CLASS_NAME, 'inspecApplyClusterSelect')).find_elements(By.NAME, 'inspecApplyClusterSelectOption')
        if len(inspecApplyClusterSelectOptions) > 0:
            for option in inspecApplyClusterSelectOptions:
                if 'xinyi_test' in option.get_attribute('title'):
                    option.click()
                    break
        webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-footer')).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createInspection'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['deleteInspection'], closeModal)
        
          # 跳转到集群列表
        sleep(1)
        
        backToClusterList()
        
        # 找到对应的测试集群
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if takeoverClusterName in activeClusterName:
                    activeCluster.click()
                    break
        else:
            util.logger.debug('未找到对应的测试集群')
            sleep(5)
            self.driver.quit()
            
        webWaitEle(self, (By.NAME, 'clusterOverviewConnectBtn'))
        sleep(1)
        for api in clusterOverviewApiKeyArr:
          util.getRequsetInfo(self, self.driver, apiDict[api], closeModal)
          
        # 单个集群 - 监控指标
        webWaitEle(self, (By.NAME, 'menu.cluster.single.monitor')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryClusterMonitorInfo'], closeModal)
        monitorBtnWrappers = self.driver.find_elements(
            By.CLASS_NAME, 'ant-radio-button-wrapper')
        monitorBtnWrappers[1].click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryClusterMonitorInfo'], closeModal)
        monitorBtnWrappers[2].click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryInpecReportList'], closeModal)
        webWaitEle(self, (By.NAME, 'execInspecBtn')).click()
        sleep(2)
        # 如果当前集群有应用巡检策略,发起巡检
        try:
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-confirm-btns')
                       ).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(3)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryInspections'], closeModal)
        except:
            pass

        sleep(2)
        
        try:
            monitorInspecReportDetailBtns = self.driver.find_elements(
                By.NAME, 'monitorInspecReportDetailBtn')
            if len(monitorInspecReportDetailBtns) > 0:
                monitorInspecReportDetailBtns[0].click()
                sleep(2)
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryClusterInspecReportDetail'], closeModal)
                allWIndowsHandles = self.driver.window_handles
                for windowHandle in allWIndowsHandles:
                    if windowHandle != mainWindowHanle:
                        self.driver.switch_to.window(windowHandle)
                        sleep(1)
                        self.driver.close()
                        sleep(1)
                        self.driver.switch_to.window(mainWindowHanle)
                        sleep(1)
        except:
            pass

        sleep(2)

        try:
            monitorInspecReportDeleteBtns = self.driver.find_elements(
                By.NAME, 'monitorInspecReportDeleteBtn')
            if len(monitorInspecReportDeleteBtns) > 0:
                monitorInspecReportDeleteBtns[0].click()
                sleep(2)
                webWaitEle(
                    self, (By.CSS_SELECTOR, 'div.monitorInspecpopconfirm button:nth-child(2)')).click()
                sleep(3)
                util.getRequsetInfo(
                    self, self.driver, apiDict['deleteClusterInspecReport'], closeModal)
        except:
            pass
        
        sleep(2)      
        # 创建告警规则
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

