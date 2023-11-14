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

from util import util

from configParams import testServer, apiDict, backupDestination, backupAK, backupSK, hostIP, alertLevels, alertTypes, opArr, alertFrequencyUnits, alertChannelTypes, alertChannelEnabled, alertChannelTempStr, backupRateLimitArr, backupConcurrencyArr, backupLogFileArr

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

        # def isElementExist(self, by, value):
        #     try:
        #         self.driver.find_element(by=by, value=value)
        #     except NoSuchElementException as e:
        #         return False
        #     return True

        # def selectComp(self, compName, optionPrefix, valueArr, callback=None):
        #     for item in valueArr:
        #         webWaitEle(self, (By.NAME, compName)).click()
        #         sleep(1)
        #         try:
        #             target = webWaitEle(self, (By.NAME, optionPrefix + item))
        #             self.driver.execute_script(
        #                 "arguments[0].scrollIntoView();", target)
        #             sleep(1)
        #             target.click()
        #         except:
        #             pass
        #         sleep(2)
        #         callback and callback(self)

        # # 开始诊断报告
        # def startDiaLog(self):
        #     self.driver.find_element(
        #         By.NAME, 'isBaseSwitch').click()
        #     sleep(2)
        #     if isElementExist(self, By.NAME, 'reportCompareStartTime'):
        #         selectTimePicker(self, 'reportCompareStartTime')
        #         self.driver.find_element(
        #             By.NAME, 'generatePerfReportBtn').click()
        #         sleep(10)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['createClusterDiagnoseReport'], closeModal)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['queryClusterDiagnoseReportStatus'], closeModal)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['queryClusterDiagnoseReportList'], closeModal)

        # # 日志检索
        # def queryLog(self):
        #     selectDate(self)
        #     performLogQuerySearchBtn = webWaitEle(
        #         self, (By.NAME, 'performLogQuerySearchBtn'))
        #     performLogQuerySearchBtn.click()
        #     sleep(3)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchTaskID'], closeModal)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchTaskList'], closeModal)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchList'], closeModal)
        #     if isElementExist(self, By.NAME, 'logDownloadShowBtn'):
        #         logDownloadShowBtn = webWaitEle(
        #             self, (By.NAME, 'logDownloadShowBtn'))
        #         logDownloadShowBtn.click()
        #         sleep(1)
        #         webWaitEle(self, (By.NAME, 'downloadLogBtn'))
        #         try:
        #             errorIconEles = self.driver.find_elements(
        #                 By.CLASS_NAME, 'anticon-close-circle')
        #             if len(errorIconEles) > 0:
        #                 webWaitEle(self, (By.NAME, 'retryLogBtn')).click()
        #                 sleep(1)
        #                 webWaitEle(self, (By.CLASS_NAME, 'ant-modal-confirm-btns')).find_element(
        #                     By.CLASS_NAME, 'ant-btn-primary').click()
        #                 sleep(1)
        #                 util.getRequsetInfo(
        #                     self, self.driver, apiDict['retryClusterLogSearchTask'], closeModal)
        #             else:
        #                 pass
        #         except:
        #             pass
        #         webWaitEle(self, (By.CLASS_NAME, 'perLogQueryDrawer')).find_element(
        #             By.CLASS_NAME, 'ant-drawer-close').click()
        #     else:
        #         pass

        # # 表格目标元素操作 confirmType 1: Confirm 2: popconfirm 3: direct
        # def handleTableOperation(self, targetEle, opBtnName, confirmType=3):
        #     parentEle = targetEle.find_element(By.XPATH, '..')
        #     grandParentEle = parentEle.find_element(By.XPATH, '..')
        #     targetOpBtnEle = grandParentEle.find_element(
        #         By.NAME, opBtnName)
        #     grandParentEle.find_element(By.NAME, opBtnName).click()
        #     sleep(1)

        #     if confirmType == 1:
        #       confirmModalEle = webWaitEle(self, (
        #         By.CLASS_NAME, 'ant-modal-confirm-body'))
        #       confirmModalEle.find_element(
        #         By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        #     elif confirmType == 2:
        #         webWaitEle(self, (
        #         By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
        #         sleep(1)
        #     elif confirmType == 3:
        #         pass

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
        updateHostModalEle.find_element(By.ID, 'UserName').send_keys('root')
        updateHostModalEle.find_element(By.ID, 'Password').send_keys('tem')
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
                # webWaitEle(self, (By.ID, 'CpuCoreNum')).send_keys('CentOS Linux 8')
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
        userNameEle.send_keys('root')
        passwordEle.send_keys('tem')
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
        sleep(1)

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

        # # 配置集群参数
        # paramTempParamsWrapperEle = webWaitEle(
        #     self, (By.CLASS_NAME, 'ant-tabs-nav-wrap'))
        # paramTypeTabs = paramTempParamsWrapperEle.find_elements(
        #     By.CLASS_NAME, 'ant-tabs-tab')
        # for index, tab in enumerate(paramTypeTabs):
        #     tabContents = self.driver.find_elements(
        #         By.CLASS_NAME, 'ant-tabs-tabpane')
        #     scrollTargetEle = self.driver.find_element(
        #         By.CLASS_NAME, 'antd-pro-pages-cluster-index-paramConfigHeaderRight')
        #     self.driver.execute_script(
        #         "arguments[0].scrollIntoView();",  scrollTargetEle)
        #     sleep(3)
        #     tab.click()
        #     tabContentBox = tabContents[index]
        #     curDeleteBtns = tabContentBox.find_elements(
        #         By.NAME, 'deleteParamBtn')
        #     randomDeleteBtn = random.choice(curDeleteBtns)
        #     self.driver.execute_script(
        #         "arguments[0].scrollIntoView();", randomDeleteBtn)
        #     sleep(1)
        #     if randomDeleteBtn:
        #         randomDeleteBtn.click()
        #     else:
        #         pass
        
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

        # 单个集群 - 参数管理
        webWaitEle(self, (By.NAME, 'menu.cluster.single.param')).click()
        sleep(5)
        util.getRequsetInfo(
            self, self.driver, apiDict['clusterParamList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateDetail'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateParams'], closeModal)

        # # 创建参数模板
        # webWaitEle(self, (By.NAME, 'createParamTemBtn')).click()
        # sleep(1)
        # webWaitEle(self, (By.NAME, 'paramTempBtn')).click()
        # sleep(1)
        # util.getRequsetInfo(
        #     self, self.driver, apiDict['queryParamTemplateList'], closeModal)

        # webWaitEle(self, (By.CLASS_NAME, 'paramTempDrawer')).find_element(
        #     By.CLASS_NAME, 'ant-drawer-close').click()
        # sleep(1)

        # webWaitEle(self, (By.ID, 'Name')).send_keys(
        #     'selenium_test_' + randomStr)
        # webWaitEle(self, (By.ID, 'Note')).send_keys(
        #     'selenium_Note_' + randomStr)

        # paramTempParamsWrapperEle = webWaitEle(
        #     self, (By.CLASS_NAME, 'ant-tabs-nav-wrap'))
        # paramTypeTabs = paramTempParamsWrapperEle.find_elements(
        #     By.CLASS_NAME, 'ant-tabs-tab')
        # for tab in paramTypeTabs:
        #     tab.click()
        #     curNodeKey = tab.get_attribute('data-node-key')
        #     for i in range(random.randint(1, 3)):
        #         webWaitEle(
        #             self, (By.NAME, 'addParamBtn_' + curNodeKey)).click()
        #     sleep(1)

        #     paramTempParamSelects = self.driver.find_elements(
        #         By.NAME, 'paramsSelect_' + curNodeKey)

        #     if len(paramTempParamSelects) > 0:
        #         for select in paramTempParamSelects:
        #             select.click()
        #             paramTempParamSelectOptions = webWaitEle(
        #                 self, (By.CLASS_NAME, 'paramsSelect_' + curNodeKey)).find_elements(By.CLASS_NAME, 'ant-select-item-option')
        #             if len(paramTempParamSelectOptions) > 0:
        #                 randomParamTempParamSelectOption = random.choice(
        #                     paramTempParamSelectOptions)
        #                 self.driver.execute_script(
        #                     "arguments[0].scrollIntoView();", randomParamTempParamSelectOption)
        #                 sleep(1)
        #                 if 'ant-select-item-option-disabled' not in randomParamTempParamSelectOption.get_attribute('class'):
        #                     randomParamTempParamSelectOption.click()
        #                     sleep(1)
        #                 else:
        #                     pass
        #             else:
        #                 pass

        #     sleep(1)

        sleep(1)
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(2)

        # 重启集群
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
                    parentEle = activeCluster.find_element(By.XPATH, '..')
                    try:
                        parentEle.find_element(By.XPATH, '..').find_element(
                            By.NAME, 'restartBtn').click()
                        sleep(1)
                        webWaitEle(self, (By.CLASS_NAME, 'clusterConfirmModal')).find_element(
                            By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
                        sleep(3)
                        util.getRequsetInfo(
                            self, self.driver, apiDict['restartCluster'], closeModal)
                        break
                    except:
                        continue

        sleep(240)  # 重启等待 4 分钟
        self.driver.refresh()

        # 找到目标集群 - 进入集群概览
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
                    activeCluster.click()
                    break
        else:
            # util.logger.debug('未找到对应的测试集群')
            sleep(5)
            self.driver.quit()
        # 进入概览页面
        webWaitEle(self, (By.NAME, 'clusterOverviewConnectBtn'))
        sleep(1)
        for api in clusterOverviewApiKeyArr:
            util.getRequsetInfo(self, self.driver, apiDict[api], closeModal)

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
        sleep(1)
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
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()

        # 找到对应的测试集群
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
                    js = "var q=document.documentElement.scrollTop=0"  # 滑动到顶部
                    self.driver.execute_script(js)
                    sleep(2)
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
            # 滑动到底部
            js = "var q=document.getElementsByClassName('relateAlertRuleDropdown')[0].getElementsByClassName('rc-virtual-list-holder-inner')[0].scrollTop=10000"
            self.driver.execute_script(js)
            for option in relateARItems:
                if testAlertRuleName in option.get_attribute('title'):
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", option)
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
        webWaitEle(self, (By.CLASS_NAME,
                   'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()
