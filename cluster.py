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

from configParams import testServer, shortCutDateIDs, shortCutName, apiDict, takeoverClusterHost, takeoverClusterPort, hostUserName, hostPwd, tiupPath, rangeStepArr, logLevelArr, backupDestination, backupAK, backupSK


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


class TestCluster(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test(self):
        def autoPage(self):
            nextPageEl = self.driver.find_element(
                By.CLASS_NAME, 'ant-table-pagination').find_element(By.CLASS_NAME, 'ant-pagination-next')
            a = nextPageEl.get_attribute('aria-disabled')
            if a == 'false':
                nextPageEl.click()
                sleep(2)

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
            randomPickerCell = random.choice(pickerCells)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomPickerCell)
            randomPickerCell.click()

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

        self.driver.get(testServer)

        mainWindowHanle = self.driver.current_window_handle

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)

        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(2)
        for api in mainPageApiArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)
        sleep(1)

        # 创建集群
        webWaitEle(self, (By.NAME, 'addClusterBtn')).click()
        clusterAliasEle = webWaitEle(self, (By.ID, 'Alias'))
        if clusterAliasEle:
            sleep(2)
            for api in addClusterApiArr:
                util.getRequsetInfo(
                    self, self.driver, apiDict[api], closeModal)
        clusterAliasEle.send_keys(
            'selenium_test_' + randomStr)
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

        # 全部随机选择
        # sizeSelectEles = clusterSizeEle.find_elements(
        #     By.CLASS_NAME, 'ant-select')
        # for sizeSelectEle in sizeSelectEles:
        #     sizeSelectEle.click()
        #     sleep(1)
        #     selectDropdownEles = self.driver.find_elements(
        #         By.CLASS_NAME, 'ant-select-dropdown')
        #     if len(selectDropdownEles) > 0:
        #         lastSelectDropdownEle = selectDropdownEles[-1]
        #         sizeOptions = lastSelectDropdownEle.find_elements(
        #             By.CLASS_NAME, 'ant-select-item-option')
        #         if len(sizeOptions) > 0:
        #             randomSizeOption = random.choice(sizeOptions)
        #             randomSizeOption.click()
        #             sleep(1)
        #         else:
        #             pass

        # 选定指定IP
        clusterIPSelectEles = clusterSizeEle.find_elements(
            By.NAME, 'clusterIPSelect')
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
                if curText.find('172.17.0.5') != -1:
                    curOption.click()
                    sleep(1)
                    break

            sleep(1)

        js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        self.driver.execute_script(js)
        sleep(3)
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

        sleep(1)

        webWaitEle(self, (By.NAME, 'previewClusterBtn')).click()


        tableHeaderEle = webWaitEle(
            self, (By.CLASS_NAME, 'ant-table-thead'))
        if tableHeaderEle:
            js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
            self.driver.execute_script(js)
            sleep(3)
            webWaitEle(self, (By.NAME, 'createClusterBtn')).click()
            util.getRequsetInfo(
                self, self.driver, apiDict['clusterAdd'], closeModal)
            sleep(5)
            
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(2)
        js = "var q=document.documentElement.scrollTop=0"  # 滑动到顶部
        self.driver.execute_script(js)
        sleep(2)

        # 纳管集群
        webWaitEle(self, (By.NAME, 'takeoverClusterBtn')).click()
        webWaitEle(self, (By.ID, 'Host')).send_keys(takeoverClusterHost)
        webWaitEle(self, (By.ID, 'Port')).send_keys(takeoverClusterPort)
        webWaitEle(self, (By.ID, 'User')).send_keys(hostUserName)
        webWaitEle(self, (By.ID, 'Password')).send_keys(hostPwd)
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
                    webWaitEle(self, (By.ID, 'UserID_' +
                               takeoverClusterName)).send_keys(hostUserName)
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
        webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        sleep(1)

        # 单个集群 - 概览
        webWaitEle(self, (By.NAME, 'takeoverClusterBtn'))
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
                    activeCluster.click()
                    break
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

        sleep(1)
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
        targetClusterIDOptions = webWaitEle(self, (By.CLASS_NAME, 'targetClusterIDSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(targetClusterIDOptions) > 0:
            randomTargetClusterIDOption = random.choice(targetClusterIDOptions)
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
        webWaitEle(self, (By.NAME, 'createParamTemBtn')).click()
        sleep(1)
        webWaitEle(self, (By.NAME, 'paramTempBtn')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['queryParamTemplateList'], closeModal)

        webWaitEle(self, (By.CLASS_NAME, 'paramTempDrawer')).find_element(
            By.CLASS_NAME, 'ant-drawer-close').click()
        sleep(1)

        webWaitEle(self, (By.ID, 'Name')).send_keys(
            'selenium_test_' + randomStr)
        webWaitEle(self, (By.ID, 'Note')).send_keys(
            'selenium_Note_' + randomStr)

        paramTempParamsWrapperEle = webWaitEle(
            self, (By.CLASS_NAME, 'ant-tabs-nav-wrap'))
        paramTypeTabs = paramTempParamsWrapperEle.find_elements(
            By.CLASS_NAME, 'ant-tabs-tab')
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

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['createParamTemplate'], closeModal)

        # 单个集群 - 集群拓扑
        webWaitEle(self, (By.NAME, 'menu.cluster.single.topology')).click()
        sleep(4)
        for api in clusterTopologyApiKeyArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)

        def operateClusterTopo(self, eleName, confirmPopName, api):
            clusterTopoEles = webWaitEle(
                self, (By.CLASS_NAME, 'ant-table-tbody')).find_elements(By.NAME, eleName)
            if len(clusterTopoEles) > 0:
                randomClusterTopoEle = random.choice(clusterTopoEles)
                randomClusterTopoEle.click()
                sleep(1)

                webWaitEle(self, (By.CLASS_NAME, confirmPopName)).find_element(
                    By.CLASS_NAME, 'ant-btn-primary').click()
                sleep(5)
                util.getRequsetInfo(
                    self, self.driver, apiDict[api], closeModal)
                sleep(30)
            else:
                pass

        # # 停止节点
        # operateClusterTopo(self, 'stopTopoNodeBtn',
        #                    'stopTopoNodePop', 'stopCluster')
        # # 启动节点
        # operateClusterTopo(self, 'startTopoNodeBtn',
        #                    'startTopoNodePop', 'startCluster')
        # # 重启节点
        # operateClusterTopo(self, 'restartTopoNodeBtn',
        #                    'restartTopoNodePop', 'restartCluster')
        scaleClusterBtn = webWaitEle(self, (By.NAME, 'scaleClusterBtn'))
        scaleClusterBtn.click()
        webWaitEle(self, (By.NAME, 'componentSelect')).click()
        sleep(1)
        componentSelectOptions = webWaitEle(self, (By.CLASS_NAME, 'componentSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        randomComponentSelectOption = random.choice(componentSelectOptions)
        randomComponentSelectOption.click()
        sleep(1)
        webWaitEle(self, (By.NAME, 'topoAddCompBtn')).click()
        sleep(1)

        webWaitEle(self, (By.NAME, 'topoScaleConfirmBtn')).click()
        sleep(3)
        util.getRequsetInfo(
            self, self.driver, apiDict['scaleCluster'], closeModal)
        if isElementExist(self, By.NAME, 'topoCancelBtn'):
            webWaitEle(self, (By.NAME, 'cancelBtn')).click()

        # 单个集群 - sql editor
        webWaitEle(self, (By.NAME, 'menu.cluster.single.sqleditor')).click()
        sleep(6)
        util.getRequsetInfo(
            self, self.driver, apiDict['querySQLEditorMeta'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['querySQLEditorStatementHistory'], closeModal)

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestCluster()
    case.test()
