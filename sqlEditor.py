# 执行变更
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from time import sleep
import random

from util import util

from configParams import testServer, apiDict, createDBText, excuteSQLText, testDBName, controlKey, excuteSQLArr

randomStr = util.get_random_string(6)

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
sqlEditorApiKeyArr = ['querySQLEditorMeta', 'querySQLEditorMetaDB', 'createSQLEditorSession', 'createSQLEditorFile', 'querySQLEditorStatementHistory', 'querySQLEditorFileList']

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
        
        # 判断元素是否存在   
        def isElementExist(self, by, value):
          try:
              self.driver.find_element(by=by, value=value)
          except NoSuchElementException as e:
              return False
          return True

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
      
        self.driver.get(testServer)

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)
        
        # 跳转到集群管理页面
        backToClusterList()
     
        # 进入集群概览
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
        
        # 单个集群 - sql 编辑器
        webWaitEle(self, (By.NAME, 'menu.cluster.single.sqleditor')).click()
        sleep(10)
        for api in sqlEditorApiKeyArr:
            util.getRequsetInfo(
                self, self.driver, apiDict[api], closeModal)
        
        # 获取codeMirror元素 -> 全选 -> 清空 -> 填充执行语句 -> 全选 -> 美化格式 -> 全选 -> 执行语句 -> 刷新数据库列表
        def getCodemirrorSendKeys(self, textArr):
            targetInputEle = webWaitEle(self, (By.CLASS_NAME, 'cm-content'))
            # 选中所有文本并清除
            targetInputEle.send_keys(controlKey, "a")
            sleep(1)
            targetInputEle.send_keys(Keys.BACKSPACE)
            sleep(1)
            # 插入文本
            for excuteSQLText in textArr:
              # text = excuteSQLText
              excuteJs = '''
                var cmContent = document.getElementsByClassName('cm-content')[0];
                var div = document.createElement('div');
                div.setAttribute('class', 'cm-line');
                div.innerHTML = '{}';
                cmContent.appendChild(div);
                '''.format(excuteSQLText)
              self.driver.execute_script(excuteJs)   
              
            sleep(1)
            #选中所有
            targetInputEle.send_keys(controlKey, "a")
            sleep(2)
            # SQL 语句美化
            beautySQLBtn = webWaitEle(self, (By.NAME, 'sqlEditorFormatBtn'))
            beautySQLBtn.click()
            sleep(2)
            # 执行语句并刷新数据库列表
            targetInputEle.send_keys(controlKey, "a")
            sleep(2)
            runSQLBtn = webWaitEle(self, (By.NAME, 'sqlEditorRunBtn'))
            runSQLBtn.click()
            sleep(5)
            util.getRequsetInfo(
                self, self.driver, apiDict['executeSQLEditorStatement'], closeModal)
            util.getRequsetInfo(
                self, self.driver, apiDict['updateSQLEditorFile'], closeModal)
            webWaitEle(self, (By.NAME, 'sqlEditorRefreshBtn')).click()
            sleep(5)
            util.getRequsetInfo(
                self, self.driver, apiDict['querySQLEditorMeta'], closeModal)
            sleep(5)
            
        #删除测试数据库
        dropTextArr = ['drop database if exists {};'.format(testDBName)]
        getCodemirrorSendKeys(self, dropTextArr)
        
        # 创建测试数据库
        getCodemirrorSendKeys(self, [createDBText])
        
        # 选中创建的测试数据库
        webWaitEle(self, (By.NAME, 'sqlEditorDBSelect')).click()
        sleep(1)
        sqlEditorDBSelectDropdownEle = webWaitEle(self, (By.CLASS_NAME, 'sqlEditorDBSelect'))
        sqlEditorDBSelectOptions = sqlEditorDBSelectDropdownEle.find_elements(By.CLASS_NAME, 'ant-select-item-option-content')
        
        if len(sqlEditorDBSelectOptions) > 0:
           for sqlEditorDBSelectOption in sqlEditorDBSelectOptions:
               sqlEditorDBSelectOptionText = util.getElementText(self, sqlEditorDBSelectOption)
               if testDBName in sqlEditorDBSelectOptionText:
                   sqlEditorDBSelectOption.click()
                   sleep(1)
                   util.getRequsetInfo(
                       self, self.driver, apiDict['createSQLEditorSession'], closeModal)
                   util.getRequsetInfo(
                       self, self.driver, apiDict['querySQLEditorFileList'], closeModal)
                   getCodemirrorSendKeys(self, excuteSQLArr)
                   break
               else:
                   pass
        else:
           pass
         
        sleep(5)
        
        # 点击执行历史
        historyBoxEle = webWaitEle(self, (By.CLASS_NAME, 'antd-pro-pages-cluster-index-queryHistoryList'))
        
        try:
          historyItems = historyBoxEle.find_elements(By.CLASS_NAME, 'antd-pro-pages-cluster-index-queryHistoryItem')
          if len(historyItems) > 0:
            firstHistoryItem = historyItems[0]
            firstHistoryItem.click()
            sleep(2)
            util.getRequsetInfo(
                self, self.driver, apiDict['executeSQLEditorStatement'], closeModal)
        except:
          pass
        
        # 查看执行信息 和 执行计划
        sleep(2)
        radiogGroupBoxEle = webWaitEle(self, (By.CLASS_NAME, 'bottomSqlTableType'))
        radioEles = radiogGroupBoxEle.find_elements(By.TAG_NAME, 'label')
        for radioEle in radioEles:
          radioEle.click()
          sleep(2)


        # 退出登录
        webWaitEle(self, (By.CLASS_NAME, 'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()

