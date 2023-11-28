# 部署全新集群
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
# import mysql.connector

from util import util

from configParams import testServer, apiDict, backupDestination, backupAK, backupSK, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr, backupRateLimitArr, backupConcurrencyArr, backupLogFileArr, SMTPAddress, SMTPUsername, SMTPPassword, SMTPSender, SMTPSenderEmail, SMTPReceiverEmail, shortCutDateIDs, shortCutName,  hostUserName, hostPwd, batchHostIP, alertEventStatus, rangeStepArr, logLevelArr, scaleHostIP, scaleCompArr

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

        def selectDate(self, cb=None):
            randomDate = random.choice(shortCutDateIDs)
            self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
            webWaitEle(self, (
                By.NAME, shortCutName.format(id=randomDate))).click()
            if cb:
                cb(self)

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

        def isElementExist(self, by, value):
            try:
                self.driver.find_element(by=by, value=value)
            except NoSuchElementException as e:
                return False
            return True

        def selectComp(self, compName, optionPrefix, valueArr, callback=None):
            for item in valueArr:
                webWaitEle(self, (By.NAME, compName)).click()
                sleep(1)
                try:
                    target = webWaitEle(self, (By.NAME, optionPrefix + item))
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", target)
                    sleep(1)
                    target.click()
                except:
                    pass
                sleep(2)
                callback and callback(self)

        # 开始诊断报告
        def startDiaLog(self):
            self.driver.find_element(
                By.NAME, 'isBaseSwitch').click()
            sleep(2)
            if isElementExist(self, By.NAME, 'reportCompareStartTime'):
                selectTimePicker(self, 'reportCompareStartTime')
                self.driver.find_element(
                    By.NAME, 'generatePerfReportBtn').click()
                sleep(10)
                util.getRequsetInfo(
                    self, self.driver, apiDict['createClusterDiagnoseReport'], closeModal)
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryClusterDiagnoseReportStatus'], closeModal)
                util.getRequsetInfo(
                    self, self.driver, apiDict['queryClusterDiagnoseReportList'], closeModal)
                sleep(2)

        # 日志检索
        def queryLog(self):
            selectDate(self)
            performLogQuerySearchBtn = webWaitEle(
                self, (By.NAME, 'performLogQuerySearchBtn'))
            performLogQuerySearchBtn.click()
            sleep(3)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryClusterLogSearchTaskID'], closeModal)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryClusterLogSearchTaskList'], closeModal)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryClusterLogSearchList'], closeModal)
            if isElementExist(self, By.NAME, 'logDownloadShowBtn'):
                logDownloadShowBtn = webWaitEle(
                    self, (By.NAME, 'logDownloadShowBtn'))
                logDownloadShowBtn.click()
                sleep(1)
                webWaitEle(self, (By.NAME, 'downloadLogBtn'))
                try:
                    errorIconEles = self.driver.find_elements(
                        By.CLASS_NAME, 'anticon-close-circle')
                    if len(errorIconEles) > 0:
                        webWaitEle(self, (By.NAME, 'retryLogBtn')).click()
                        sleep(1)
                        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-confirm-btns')).find_element(
                            By.CLASS_NAME, 'ant-btn-primary').click()
                        sleep(1)
                        util.getRequsetInfo(
                            self, self.driver, apiDict['retryClusterLogSearchTask'], closeModal)
                    else:
                        pass
                except:
                    pass
                webWaitEle(self, (By.CLASS_NAME, 'perLogQueryDrawer')).find_element(
                    By.CLASS_NAME, 'ant-drawer-close').click()
            else:
                pass

        # 滑动到顶部
        def scrollToTop(self):
            js = "var q=document.documentElement.scrollTop=0"
            self.driver.execute_script(js)
            sleep(2)

        # 表格目标元素操作 confirmType 1: Confirm 2: popconfirm 3: direct
        def handleTableOperation(self, targetEle, opBtnName, confirmType=3):
            parentEle = targetEle.find_element(By.XPATH, '..')
            grandParentEle = parentEle.find_element(By.XPATH, '..')
            targetOpBtnEle = grandParentEle.find_element(
                By.NAME, opBtnName)
            grandParentEle.find_element(By.NAME, opBtnName).click()
            sleep(1)

            if confirmType == 1:
                confirmModalEle = webWaitEle(self, (
                    By.CLASS_NAME, 'ant-modal-confirm-body'))
                confirmModalEle.find_element(
                    By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            elif confirmType == 2:
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
                sleep(1)
            elif confirmType == 3:
                pass

        # 返回集群列表
        def backToClusterList():
            sleep(2)
            webWaitEle(self, (By.NAME, 'menu.cluster')).click()
            for api in mainPageApiArr:
                util.getRequsetInfo(
                    self, self.driver, apiDict[api], closeModal)
            sleep(2)
            scrollToTop(self)

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

        def __selectDate(self):
            randomDate = random.choice(shortCutDateIDs)
            self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
            webWaitEle(self, (
                By.NAME, shortCutName.format(id=randomDate))).click()

        self.driver.get(testServer)

        mainWindowHanle = self.driver.current_window_handle

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)

        webWaitEle(self, (By.NAME, 'menu.host')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryHostList'], closeModal)

        randomStr = util.get_random_string(6)
        createClusterName = 'selenium_test_' + randomStr

        # 创建主机和主机规格
        webWaitEle(self, (By.NAME, 'createHostBtn')).click()
        updateHostModalEle = webWaitEle(self, (
            By.CLASS_NAME, 'updateHostModal'))
        updateHostModalEle.find_element(By.ID, 'IP').send_keys(hostIP)
        updateHostModalEle.find_element(
            By.ID, 'UserName').send_keys(hostUserName)
        updateHostModalEle.find_element(By.ID, 'Password').send_keys(hostPwd)
        updateHostModalEle.find_element(By.ID, 'SSHPort').send_keys('22')

        webWaitEle(self, (By.NAME, 'hostModalFindBtn')).click()
        util.getRequsetInfo(
            self, self.driver, apiDict['discoverHost'], closeModal)

        hostModalSaveSpecBtn = webWaitEle(self, (
            By.NAME, 'hostModalSaveSpecBtn'))

        if hostModalSaveSpecBtn:
            hostModalSaveSpecBtn.click()
            hostSpecDrawerEle = webWaitEle(self, (
                By.CLASS_NAME, 'ant-drawer-content-wrapper'))
            if hostSpecDrawerEle:
                webWaitEle(self, (By.ID, 'Name')).send_keys(
                    'selenium_test_' + randomStr)
                webWaitEle(self, (By.NAME, 'hostDawerCpuArchSelect')).click()
                cpuArchs = self.driver.find_elements(
                    By.CLASS_NAME, 'ant-select-item-option')
                random.choice(cpuArchs).click()
                # webWaitEle(self, (By.ID, 'CpuModel')).send_keys('Kunpeng-920')
                cpuCoresEle = webWaitEle(self, (By.ID, 'CpuCores'))
                util.clearInput(cpuCoresEle)
                cpuCoresEle.send_keys(random.randint(1, 64))
                webWaitEle(self, (By.ID, 'Notes')).send_keys(
                    'selenium_test_note_' + randomStr)
                webWaitEle(self, (By.NAME, 'hostrDawerSaveSpecBtn')).click()
                sleep(2)
                util.getRequsetInfo(
                    self, self.driver, apiDict['createSpec'], closeModal)

        saveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')
                                 ).find_element(By.CLASS_NAME, 'ant-btn-primary')
        if saveHostBtn.get_attribute('disabled'):
            return
        else:
            saveHostBtn.click()
            sleep(2)
            util.getRequsetInfo(
                self, self.driver, apiDict['createHost'], closeModal)
        sleep(1)

        # 编辑主机
        testHostEle = webWaitEle(
            self, (By.XPATH, "//*[contains(text(), '172.17.0.17')]"))
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",  testHostEle)
        sleep(1)
        parentEle = testHostEle.find_element(By.XPATH, '..')
        grandParentEle = parentEle.find_element(By.XPATH, '..')
        grandParentEle.find_element(By.NAME, 'updateHostBtn').click()
        userNameEle = webWaitEle(self, (By.ID, 'UserName'))
        passwordEle = webWaitEle(self, (By.ID, 'Password'))
        sshPortEle = webWaitEle(self, (By.ID, 'SSHPort'))
        util.clearInput(userNameEle)
        util.clearInput(passwordEle)
        util.clearInput(sshPortEle)
        userNameEle.send_keys(hostUserName)
        passwordEle.send_keys(hostPwd)
        sshPortEle.send_keys('22')
        webWaitEle(self, (By.NAME, 'hostModalFindBtn')).click()
        sleep(5)
        util.getRequsetInfo(
            self, self.driver, apiDict['discoverHost'], closeModal)
        saveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')
                                 ).find_element(By.CLASS_NAME, 'ant-btn-primary')
        if saveHostBtn.get_attribute('disabled'):
            return
        else:
            saveHostBtn.click()
            sleep(2)
            util.getRequsetInfo(
                self, self.driver, apiDict['updateHost'], closeModal)
        sleep(10)

        # 主机详情
        sleep(2)
        testHostEle.click()
        util.getRequsetInfo(
            self, self.driver, apiDict['queryHostMonitor'], closeModal)
        sleep(1)
        hostDetailCloseBtn = webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-content')).find_element(By.CLASS_NAME, 'ant-modal-close')
        hostDetailCloseBtn.click()
        sleep(1)

        scrollToTop(self)

        # 批量添加主机
        webWaitEle(self, (By.NAME, 'batchAddHostBtn')).click()
        sleep(1)
        webWaitEle(self, (By.ID, 'UserName')).send_keys(hostUserName)
        webWaitEle(self, (By.ID, 'Password')).send_keys(hostPwd)
        webWaitEle(self, (By.ID, 'SSHPort')).send_keys('22')
        webWaitEle(self, (By.ID, 'HostList')).send_keys(batchHostIP)
        webWaitEle(self, (By.NAME, 'batchAddHostTestBtn')).click()
        sleep(3)
        util.getRequsetInfo(
            self, self.driver, apiDict['discoverHost'], closeModal)

        batchSaveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'batchAddHostModal')).find_element(
            By.CLASS_NAME, 'ant-modal-footer').find_element(By.CLASS_NAME, 'ant-btn-primary')
        if batchSaveHostBtn.get_attribute('disabled'):
            return
        else:
            batchSaveHostBtn.click()
            sleep(2)
            util.getRequsetInfo(
                self, self.driver, apiDict['createHost'], closeModal)
        sleep(1)

        # 主机规格管理
        webWaitEle(self, (By.NAME, 'hostSpecManageBtn')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['querySpecList'], closeModal)

        def updateSpecInfo(self, isCreate=False):
            cpuModelEle = webWaitEle(self, (By.ID, 'CpuModel'))
            osEle = webWaitEle(self, (By.ID, 'OS'))
            cpuCoresEle = webWaitEle(self, (By.ID, 'CpuCores'))
            memoryEle = webWaitEle(self, (By.ID, 'Memory'))
            storageEle = webWaitEle(self, (By.ID, 'Storage'))
            notesEle = webWaitEle(self, (By.ID, 'Notes'))
            if isCreate == False:
                util.clearInput(cpuModelEle)
                util.clearInput(osEle)
                util.clearInput(cpuCoresEle)
                util.clearInput(memoryEle)
                util.clearInput(storageEle)
                util.clearInput(notesEle)

            webWaitEle(self, (By.NAME, 'hostDawerCpuArchSelect')).click()
            cpuArchs = webWaitEle(self, (By.CLASS_NAME, 'hostDawerCpuArchSelect')).find_elements(
                By.CLASS_NAME, 'ant-select-item-option')
            random.choice(cpuArchs).click()
            cpuModelEle.send_keys('Kunpeng-920')
            osEle.send_keys('CentOS Linux 8')
            webWaitEle(self, (By.NAME, 'hostDrawerDiskTypeSelect')).click()
            diskTypes = webWaitEle(self, (By.CLASS_NAME, 'hostDrawerDiskTypeSelect')).find_elements(
                By.CLASS_NAME, 'ant-select-item-option')
            random.choice(diskTypes).click()
            cpuCoresEle.send_keys(random.randint(1, 32))
            memoryEle.send_keys(random.randint(1, 128))
            storageEle.send_keys(random.randint(1, 1024))
            notesEle.send_keys('selenium_test_note_' + randomStr)

            webWaitEle(self, (By.CLASS_NAME, 'antd-pro-pages-host-manage-index-customFooter')
                       ).find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            if isCreate:
                util.getRequsetInfo(
                    self, self.driver, apiDict['createSpec'], closeModal)
            else:
                util.getRequsetInfo(
                    self, self.driver, apiDict['updateSpec'], closeModal)

        # 创建主机规格
        webWaitEle(self, (By.NAME, 'addHostSpecBtn')).click()
        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_test_' + randomStr)
        updateSpecInfo(self, True)

        # 编辑主机规格
        updateHostSpecBtns = self.driver.find_elements(
            By.NAME, 'updateHostSpecBtn')
        firstUpdateHostSpecBtn = updateHostSpecBtns[0]
        if firstUpdateHostSpecBtn:
            firstUpdateHostSpecBtn.click()
            sleep(1)
            updateSpecInfo(self)
            sleep(1)

        # 删除主机规格
        deleteHostSpecBtns = self.driver.find_elements(
            By.NAME, 'deleteHostSpecBtn')
        firstDeleteHostSpecBtn = deleteHostSpecBtns[0]
        if firstDeleteHostSpecBtn:
            firstDeleteHostSpecBtn.click()
            sleep(1)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.hostSpecDeletePopconfirm  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['deleteSpec'], closeModal)

        # 集群管理
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(2)
        for api in mainPageApiArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)
        sleep(1)

        # 创建集群
        webWaitEle(self, (By.NAME, 'addClusterBtn')).click()
        clusterAliasEle = webWaitEle(self, (By.ID, 'Alias'))

        # 创建集群的名称
        if clusterAliasEle:
            sleep(2)
            for api in addClusterApiArr:
                util.getRequsetInfo(
                    self, self.driver, apiDict[api], closeModal)
        clusterAliasEle.send_keys(createClusterName)
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
            for opIndex, curOption in enumerate(curOptions):
                contentEle = curOption.find_element(
                    By.CLASS_NAME, 'ant-select-item-option-content')
                curText = util.getElementText(self, contentEle)
                if curText.find(hostIP) != -1:
                    curOption.click()
                    sleep(1)
                    break
                elif opIndex == len(curOptions) - 1:
                    clusterIPSelectEle.click()
                    isTargetIP = False
                    break

            sleep(1)

        js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        self.driver.execute_script(js)
        sleep(3)

        if isTargetIP:
            js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
            self.driver.execute_script(js)
            sleep(3)

            webWaitEle(self, (By.NAME, 'previewClusterBtn')).click()

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

        # sleep(180) # 等待 3 分钟 等待集群创建成功
        backToClusterList()

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
        fillBackupAdvancedOptions(self)

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['backupCluster'], closeModal)
        # 等待十秒备份
        sleep(10)

        scrollToTop(self)
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
                    # print('backupNameEles---->',len(backupNameEles))
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
        sleep(1)
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

        fillBackupAdvancedOptions(self)

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createBackupPolicy'], closeModal)

        sleep(10)

        # 编辑备份策略
        webWaitEle(self, (By.NAME, 'backupPolicyEditBtn'))
        editBtns = self.driver.find_elements(
            By.NAME, 'backupPolicyEditBtn')
        if len(editBtns) > 0:
            lastEditBtn = editBtns[-1]
            lastEditBtn.click()
            sleep(1)
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

            fillBackupAdvancedOptions(self)

            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['updateBackupPolicy'], closeModal)
        else:
            pass

        sleep(10)

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
        else:
            pass

        # 告警管理
        webWaitEle(self, (By.NAME, 'menu.alert')).click()

        # 告警事件

        # 告警规则
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
            util.getRequsetInfo(
                self, self.driver, apiDict['updateAlertRule'], closeModal)
            sleep(2)
        # 启用停用告警规则
        scrollToTop(self)
        sleep(2)
        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((
            By.NAME, 'alertRulesStatusBtn')))
        statusBtn = webWaitEle(self, (
            By.NAME, 'alertRulesStatusBtn'))
        if statusBtn:
            statusBtn.click()
            sleep(2)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo(
                self, self.driver,  apiDict['switchAlertRuleStatus'], closeModal)
            sleep(2)
            statusBtn.click()
            # sleep(2)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
            util.getRequsetInfo(
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
        util.getRequsetInfo(
            self, self.driver, apiDict['deleteAlertRule'], closeModal)
        sleep(5)

        # 告警通道
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

        webWaitEle(self, (
            By.ID, 'Name')).send_keys('selenium_test_' + randomStr)
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
            deleteBtn = curOpBox.find_element(
                By.NAME, 'alertChannelDeleteBtn')
            if deleteBtn:
                deleteBtn.click()
                sleep(1)
                webWaitEle(self, (
                    By.CSS_SELECTOR, 'div.alertChannelDeletePopconfirm  button:nth-child(2)')).click()
                sleep(1)
                util.getRequsetInfo(
                    self, self.driver, apiDict['deleteAlertChannel'], closeModal)
        else:
            pass

        sleep(2)

        # 告警事件
        webWaitEle(self, (By.NAME, 'menu.alert.event')).click()
        sleep(12)  # 告警事件请求时间较长
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
                    sleep(12)
                    util.getRequsetInfo(
                        self, self.driver, apiDict['queryAlertEventList'], closeModal)

        sleep(2)

        backToClusterList()

        # 单个集群 - 概览
        # 找到测试的集群
        def findTestCluster():
            webWaitEle(self, (By.NAME, 'takeoverClusterBtn'))
            activeClusters = self.driver.find_elements(
                By.CLASS_NAME, 'clusterAlias')
            if len(activeClusters) > 0:
                for activeCluster in activeClusters:
                    activeClusterName = util.getElementText(
                        self, activeCluster)
                    if createClusterName == activeClusterName:
                        activeCluster.click()
                        break
                    elif 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
                        activeCluster.click()
                        break
            webWaitEle(self, (By.NAME, 'clusterOverviewConnectBtn'))

            sleep(1)
            for api in clusterOverviewApiKeyArr:
                util.getRequsetInfo(self, self.driver,
                                    apiDict[api], closeModal)

        findTestCluster()

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

        # 单个集群 - 性能诊断
        webWaitEle(self, (By.NAME, 'menu.cluster.single.performance')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryClusterTopSqlList'], closeModal)
        perfRadioBtns = self.driver.find_elements(
            By.CLASS_NAME, 'ant-radio-button-wrapper')
        # 慢查询
        perfRadioBtns[1].click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryClusterSlowQueryList'], closeModal)
        # 诊断报告
        perfRadioBtns[2].click()
        sleep(2)
        selectTimePicker(self, 'reportStartTime')
        sleep(1)
        selectComp(self, 'rangeStep', 'rangeStep_', rangeStepArr, startDiaLog)
        # 日志检索
        perfRadioBtns[3].click()
        sleep(3)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryClusterLogSearchTopology'], closeModal)
        selectComp(self, 'logInfoType', 'logInfoType_', logLevelArr, queryLog)
        sleep(1)

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

        # 单个集群 - 参数管理
        webWaitEle(self, (By.NAME, 'menu.cluster.single.param')).click()
        sleep(5)
        util.getRequsetInfo(
            self, self.driver, apiDict['clusterParamList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateDetail'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateParams'], closeModal)

        sleep(1)

        # 单个集群 - 集群拓扑
        webWaitEle(self, (By.NAME, 'menu.cluster.single.topology')).click()
        sleep(2)
        for api in clusterTopologyApiKeyArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)

        # 扩容集群
        scaleClusterBtn = webWaitEle(self, (By.NAME, 'scaleClusterBtn'))
        scaleClusterBtn.click()
        sleep(1)

        if isElementExist(self, By.CLASS_NAME, 'noHostResourceTipModal'):
            noResourceModalEle = webWaitEle(
                self, (By.CLASS_NAME, 'noHostResourceTipModal'))
            noResourceModalEle.find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
        else:
            isTargetIP = True
            for comp in scaleCompArr:
                sleep(2)
                webWaitEle(self, (By.NAME, 'componentSelect')).click()
                sleep(2)
                compSelectOptions = webWaitEle(self, (By.CLASS_NAME, 'componentSelect')).find_elements(
                    By.CLASS_NAME, 'ant-select-item-option')

                # 添加 tikv / tidb / pd / tiflash 节点
                for compSelectOption in compSelectOptions:
                    compTitle = compSelectOption.get_attribute('title')
                    if comp == compTitle:
                        compSelectOption.click()
                        sleep(1)
                        scaleIPSelectEle = webWaitEle(
                            self, (By.NAME, 'topoHostSelect'))
                        scaleIPSelectEle.click()
                        sleep(1)
                        clusterIPSelectDropdownEle = self.driver.find_element(
                            By.CLASS_NAME, 'topoHostSelect')
                        curOptions = clusterIPSelectDropdownEle.find_elements(
                            By.CLASS_NAME, 'ant-select-item-option')
                        for opIndex, curOption in enumerate(curOptions):
                            contentEle = curOption.find_element(
                                By.CLASS_NAME, 'ant-select-item-option-content')
                            curText = util.getElementText(self, contentEle)
                            if curText == scaleHostIP:
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView();",  curOption)
                                sleep(1)
                                curOption.click()
                                sleep(1)
                                break
                            elif opIndex == len(curOptions) - 1:
                                scaleIPSelectEle.click()
                                isTargetIP = False
                                break
                            else:
                                pass

                topoAddCompBtn = webWaitEle(self, (By.NAME, 'topoAddCompBtn'))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", topoAddCompBtn)
                sleep(1)
                topoAddCompBtn.click()
                sleep(1)

            if isTargetIP:
                sleep(1)
                webWaitEle(self, (By.NAME, 'topoScaleConfirmBtn')).click()
                sleep(5)
                util.getRequsetInfo(
                    self, self.driver, apiDict['scaleCluster'], closeModal)
                sleep(180)  # 等待集群扩容完成 3 分钟
            else:
                closeModal(self)

        # 缩容集群
        def findScaleInClusterEle(self, compName, opBtnName):
            classStr = '%sChildTable' % compName
            compTableEle = webWaitEle(self, (By.CLASS_NAME, classStr))
            try:
                compEle = compTableEle.find_element(
                    By.XPATH, ".//*[contains(text(),'%s')]" % scaleHostIP)
                compParentEle = compEle.find_element(
                    By.XPATH, "../..").find_element(By.NAME, opBtnName)
                return compParentEle
            except:
                return None

        # 展开需要删除的组件
        topoExpandComsArr = ['TiKV', 'TiDB', 'PD', 'TiFlash']

        for topoExpandCom in topoExpandComsArr:
            try:
                compExpandEle = webWaitEle(
                    self, (By.NAME, '%s_plus' % topoExpandCom))
                compExpandEle.click()
                sleep(2)
            except:
                pass

        # 找到目标组件 删除操作
        topoDeleteComsArr = ['tikv', 'tidb', 'pd', 'tiflash']
        for topoDeleteCom in topoDeleteComsArr:
            try:
                compEle = findScaleInClusterEle(
                    self, topoDeleteCom, 'deleteTopoNodeBtn')
                if compEle != None:
                    compEle.click()
                    sleep(2)
                    webWaitEle(self, (By.CLASS_NAME, 'deleteTopoNodeModal')).find_element(
                        By.CLASS_NAME, 'ant-btn-primary').click()
                    sleep(5)
                    util.getRequsetInfo(
                        self, self.driver, apiDict['scaleCluster'], closeModal)
                    sleep(180)
                else:
                    pass
            except:
                pass

        # SQL 编辑器
        # 待补充

        # 修改巡检策略
        # 滚动到页面顶部
        scrollToTop(self)

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
        sleep(5)

        #  巡检策略详情
        inspecPolicyAliasBtns = self.driver.find_elements(
            By.NAME, 'inspecPolicyAliasBtn')
        js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        self.driver.execute_script(js)
        sleep(3)
        lastPolicyAliasBtn = inspecPolicyAliasBtns[-1]

        # randomPolicyAliasBtn = random.choice(inspecPolicyAliasBtns)
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", randomPolicyAliasBtn)
        # sleep(1)
        # randomPolicyAliasBtn.click()

        lastPolicyAliasBtn.click()
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
        sleep(2)

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
        sleep(2)

        # 参数组模板
        # 滚动到页面顶部
        scrollToTop(self)

        webWaitEle(self, (By.NAME, 'headSettingIcon')).click()
        sleep(1)
        webWaitEle(
            self, (By.CLASS_NAME, 'headerSettingDropdown')).find_element(By.NAME, 'menu.paramstemplate').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateParams'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['clusterList'], closeModal)
        self.driver.find_element(By.TAG_NAME, 'body').click()
        sleep(1)

        # 创建参数组模板
        webWaitEle(self, (By.NAME, 'createParamTempBtn')).click()
        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_test_' + randomStr)
        webWaitEle(
            self, (By.NAME, 'paramsTempClusterVersionSelect')).click()
        paramsTempClusterVersionOptions = webWaitEle(
            self, (By.CLASS_NAME, 'paramsTempClusterVersionSelect')).find_elements(By.CLASS_NAME, 'ant-select-item-option')
        if len(paramsTempClusterVersionOptions) > 0:
            randomParamsTempClusterVersionOption = random.choice(
                paramsTempClusterVersionOptions)
            randomParamsTempClusterVersionOption.click()
        webWaitEle(self, (By.ID, 'Note')).send_keys(
            'selenium_Note_' + randomStr)
        webWaitEle(
            self, (By.NAME, 'paramsTempApplyClustersSelect')).click()
        paramsTempApplyClustersOptions = webWaitEle(
            self, (By.CLASS_NAME, 'paramsTempApplyClustersSelect')).find_elements(By.CLASS_NAME, 'ant-select-item-option')
        if len(paramsTempApplyClustersOptions) > 0:
            for option in paramsTempApplyClustersOptions:
                if 'xinyi_test' in option.get_attribute('title') and 'ant-select-item-option-disabled' not in option.get_attribute('class'):
                    option.click()
                    break
        paramTempParamsWrapperEle = webWaitEle(
            self, (By.CLASS_NAME, 'ant-tabs-nav-wrap'))
        paramTypeTabs = paramTempParamsWrapperEle.find_elements(
            By.CLASS_NAME, 'ant-tabs-tab')
        for tab in paramTypeTabs:
            tab.click()
            curNodeKey = tab.get_attribute('data-node-key')
            for i in range(random.randint(1, 3)):
                webWaitEle(
                    self, (By.NAME, 'addParamBtn_' + curNodeKey)).click()
            sleep(1)

            paramTempParamSelects = self.driver.find_elements(
                By.NAME, 'paramsSelect_' + curNodeKey)

            if len(paramTempParamSelects) > 0:
                for select in paramTempParamSelects:
                    select.click()
                    paramTempParamSelectOptions = webWaitEle(
                        self, (By.CLASS_NAME, 'paramsSelect_' + curNodeKey)).find_elements(By.CLASS_NAME, 'ant-select-item-option')
                    if len(paramTempParamSelectOptions) > 0:
                        randomParamTempParamSelectOption = random.choice(
                            paramTempParamSelectOptions)
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView();", randomParamTempParamSelectOption)
                        sleep(1)
                        if 'ant-select-item-option-disabled' not in randomParamTempParamSelectOption.get_attribute('class'):
                            randomParamTempParamSelectOption.click()
                            sleep(1)
                        else:
                            pass
                    else:
                        pass

            sleep(1)

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createParamTemplate'], closeModal)

        # 参数组模板详情
        paramTempNameBtns = self.driver.find_elements(
            By.NAME, 'paramTempNameBtn')
        randomparamTempNamBtn = random.choice(paramTempNameBtns)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomparamTempNamBtn)
        randomparamTempNamBtn.click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateDetail'], closeModal)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-close-x')).click()
        sleep(1)

        # 编辑参数组模板
        updateParamTempBtns = self.driver.find_elements(
            By.NAME, 'updateParamTempBtn')
        lastupdateParamTempBtn = updateParamTempBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastupdateParamTempBtn)
        sleep(1)
        lastupdateParamTempBtn.click()
        sleep(1)
        paramTempModalName = webWaitEle(self, (By.ID, 'Name'))
        util.clearInput(paramTempModalName)
        paramTempModalName.send_keys('selenium_test_' + randomStr)
        paramTempModalDesc = webWaitEle(self, (By.ID, 'Note'))
        util.clearInput(paramTempModalDesc)
        paramTempModalDesc.send_keys('selenium_Note_' + randomStr)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-confirm-btns')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['updateParamTemplate'], closeModal)

        # 删除参数组模板
        deleteParamTempBtns = self.driver.find_elements(
            By.NAME, 'deleteParamTempBtn')
        lastdeleteParamTempBtn = deleteParamTempBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastdeleteParamTempBtn)
        sleep(1)
        if lastdeleteParamTempBtn:
            lastdeleteParamTempBtn.click()
            sleep(1)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-modal-confirm-btns  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['deleteParamTemplate'], closeModal)

        sleep(5)

        # 系统审计
       # 审计配置
        auditSwitchEle = webWaitEle(self, (By.NAME, 'auditSwitch'))

        def changeAuditStatus(self, cb=None):
            auditSwitchStatus = auditSwitchEle.get_attribute('aria-checked')
            if auditSwitchStatus == 'true':
                cb and cb(self)
                sleep(1)
            auditSwitchStatusApi = 'enableAudit' if auditSwitchStatus == 'false' else 'disableAudit'
            auditSwitchEle.click()
            sleep(1)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-modal-confirm-btns  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict[auditSwitchStatusApi], closeModal)

        def setSeleniumAudit(self):
            auditUsers = self.driver.find_elements(
                By.CLASS_NAME, 'antd-pro-pages-audit-index-userItem')
            for user in auditUsers:
                if 'selenium_test1' in util.getElementText(self, user):
                    user.click()
                    break

            auditCheckWrapperEles = self.driver.find_elements(
                By.CLASS_NAME, 'ant-checkbox-wrapper')
            randomCheckWrapperEle = random.choice(auditCheckWrapperEles)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomCheckWrapperEle)
            sleep(1)
            randomCheckWrapperEle.click()
            webWaitEle(self, (By.CLASS_NAME, 'antd-pro-pages-audit-index-bottomBtnBox')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-modal-confirm-btns  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['updateAuditConfig'], closeModal)

        changeAuditStatus(self, setSeleniumAudit)
        changeAuditStatus(self, setSeleniumAudit)

        sleep(3)

        # 审计日志
        webWaitEle(self, (By.NAME, 'menu.audit.log')).click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAuditLogOption'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryAuditLog'], closeModal)

        for d in shortCutDateIDs:
            webWaitEle(self, (By.NAME, 'rangePickerShortcut')).click()
            sleep(2)
            webWaitEle(self, (
                By.NAME, shortCutName.format(id=d))).click()
            sleep(2)
            webWaitEle(self, (By.NAME, 'auditLogSearchBtn')).click()
            sleep(3)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryAuditLog'], closeModal)
        sleep(5)

        # 任务流
        webWaitEle(self, (By.NAME, 'menu.taskflow')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryTaskFlowList'], closeModal)
        taskflowDetailBtns = self.driver.find_elements(
            By.NAME, 'taskflowDetailBtn')
        if len(taskflowDetailBtns) > 0:
            randomTaskflowDetailBtn = random.choice(taskflowDetailBtns)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomTaskflowDetailBtn)
            sleep(1)
            randomTaskflowDetailBtn.click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['queryTaskFlowDetail'], closeModal)
            sleep(1)
            taskflowDetailCloseBtn = webWaitEle(self, (
                By.CLASS_NAME, 'ant-modal-content')).find_element(By.CLASS_NAME, 'ant-modal-close')
            taskflowDetailCloseBtn.click()
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
