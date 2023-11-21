# 执行变更
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

from configParams import testServer, apiDict, scaleCompArr, scaleHostIP, hostIP

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

        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)
        
        # 跳转到集群管理页面
        backToClusterList()
        
       # 创建集群
        # testClusterName = 'selenium_test_' + randomStr
        testClusterName = 'xinyi_test_1116_01'
        # webWaitEle(self, (By.NAME, 'addClusterBtn')).click()
        # sleep(1)
        # clusterAliasEle = webWaitEle(self, (By.ID, 'Alias'))
        # if clusterAliasEle:
        #     sleep(2)
        #     for api in addClusterApiArr:
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict[api], closeModal)
        # clusterAliasEle.send_keys(testClusterName)
        # webWaitEle(self, (By.ID, 'Password')).send_keys('tem')
        # webWaitEle(self, (By.NAME, 'clusterVersionSelect')).click()
        # sleep(1)
        # clusterVersionOptions = webWaitEle(self, (By.CLASS_NAME, 'clusterVersionSelect')).find_elements(
        #     By.CLASS_NAME, 'ant-select-item-option')
        # randomClusterVersionOption = random.choice(clusterVersionOptions)
        # randomClusterVersionOption.click()
        # sleep(1)
        # webWaitEle(self, (By.NAME, 'clusterArchSelect')).click()
        # sleep(1)
        # clusterArchOptions = webWaitEle(self, (By.CLASS_NAME, 'clusterArchSelect')).find_elements(
        #     By.CLASS_NAME, 'ant-select-item-option')
        # randomClusterArchOption = random.choice(clusterArchOptions)
        # randomClusterArchOption.click()
        # sleep(1)

        # clusterModelEle = webWaitEle(self, (By.ID, 'Model'))
        # shareClusterModelEle = clusterModelEle.find_element(
        #     By.CSS_SELECTOR, 'label.ant-radio-button-wrapper:nth-child(2)')
        # shareClusterModelEle.click()
        # clusterCollapseHeaders = self.driver.find_elements(
        #     By.CLASS_NAME, 'ant-collapse-header')
        # for clusterCollapseHeader in clusterCollapseHeaders:
        #     if clusterCollapseHeader.get_attribute('aria-expanded') == 'false':
        #         clusterCollapseHeader.click()
        #         sleep(1)

        # js = "var q=document.documentElement.scrollTop=0"
        # self.driver.execute_script(js)
        # sleep(3)
        # # 选择规模信息
        # clusterSizeEle = webWaitEle(self, (By.ID, 'clusterSizeInfo'))
        # deleteSizeInfoBtns = clusterSizeEle.find_elements(
        #     By.NAME, 'deleteSizeInfoBtn')
        # for deleteSizeInfoBtn in deleteSizeInfoBtns:
        #     deleteSizeInfoBtn.click()
        #     sleep(1)

        # sleep(1)
        
        # # 选定指定IP
        # clusterIPSelectEles = clusterSizeEle.find_elements(
        #     By.NAME, 'clusterIPSelect')
        # isTargetIP = True
        # for index, clusterIPSelectEle in enumerate(clusterIPSelectEles):
        #     clusterIPSelectEle.click()
        #     sleep(1)
        #     clusterIPSelectDropdownEles = self.driver.find_elements(
        #         By.CLASS_NAME, 'clusterIPSelect')
        #     curOptions = clusterIPSelectDropdownEles[index].find_elements(
        #         By.CLASS_NAME, 'ant-select-item-option')
        #     for opIndex, curOption in enumerate(curOptions):
        #         contentEle = curOption.find_element(
        #             By.CLASS_NAME, 'ant-select-item-option-content')
        #         curText = util.getElementText(self, contentEle)
        #         if curText.find(hostIP) != -1:
        #             curOption.click()
        #             sleep(1)
        #             break
        #         elif opIndex == len(curOptions) - 1:
        #             clusterIPSelectEle.click()
        #             isTargetIP = False
        #             break

        #     sleep(1)

        # js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        # self.driver.execute_script(js)
        # sleep(3)
        # if isTargetIP:
        #   js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        #   self.driver.execute_script(js)
        #   sleep(3)

        #   webWaitEle(self, (By.NAME, 'previewClusterBtn')).click()

        #   if isElementWaitExist(self, (By.CLASS_NAME, 'ant-table-thead')):
        #       js = "var q=document.documentElement.scrollTop=10000"  # 滑动到底部
        #       self.driver.execute_script(js)
        #       sleep(3)
        #       webWaitEle(self, (By.NAME, 'createClusterBtn')).click()
        #       sleep(30)
        #       util.getRequsetInfo(
        #           self, self.driver, apiDict['clusterAdd'], closeModal)
        #       sleep(180)
              
        #       # webWaitEle(self, (By.NAME, 'menu.cluster')).click()
        #       # sleep(2)
        #       # js = "var q=document.documentElement.scrollTop=0"  # 滑动到顶部
        #       # self.driver.execute_script(js)
        #       # sleep(2)
        #   else: 
        #      backToClusterList()
        # else:
        #   backToClusterList()
        #   pass
              
            
        # 进入集群概览
        # 找到目标集群 - 进入集群概览
        activeClusters = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')
        if len(activeClusters) > 0:
            for activeCluster in activeClusters:
                activeClusterName = util.getElementText(self, activeCluster)
                if testClusterName in activeClusterName or 'xinyi_test' in activeClusterName or 'selenium_test' in activeClusterName:
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
        
        
        # 单个集群 - 集群拓扑
        webWaitEle(self, (By.NAME, 'menu.cluster.single.topology')).click()
        sleep(1)
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
                sleep(120)
            else:
                pass
        
        # 扩容集群      
        scaleClusterBtn = webWaitEle(self, (By.NAME, 'scaleClusterBtn'))
        scaleClusterBtn.click()
        sleep(1)
        
        if isElementExist(self, By.CLASS_NAME, 'noHostResourceTipModal'):
          noResourceModalEle = webWaitEle(self, (By.CLASS_NAME, 'noHostResourceTipModal'))
          noResourceModalEle.find_element(By.CLASS_NAME, 'ant-btn-primary').click()
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
                scaleIPSelectEle = webWaitEle(self, (By.NAME, 'topoHostSelect'))
                
                clusterIPSelectDropdownEle = self.driver.find_element(
                    By.CLASS_NAME, 'topoHostSelect')
                curOptions = clusterIPSelectDropdownEle.find_elements(
                    By.CLASS_NAME, 'ant-select-item-option')
                for opIndex, curOption in enumerate(curOptions):
                  contentEle = curOption.find_element(
                      By.CLASS_NAME, 'ant-select-item-option-content')
                  curText = util.getElementText(self, contentEle)
                  if curText == scaleHostIP:
                      self.driver.execute_script( "arguments[0].scrollIntoView();",  curOption)
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
                    
            webWaitEle(self, (By.NAME, 'topoAddCompBtn')).click()
            sleep(1)
          
                
          if isTargetIP:
            sleep(1)
            webWaitEle(self, (By.NAME, 'topoScaleConfirmBtn')).click()
            sleep(5)
            util.getRequsetInfo(
                self, self.driver, apiDict['scaleCluster'], closeModal)
            sleep(180) # 等待集群扩容完成 3 分钟
          else:
              pass
              
        # 缩容集群
        def findScaleInClusterEle(self, compName, opBtnName):
          classStr = '%sChildTable' % compName
          compTableEle = webWaitEle(self, (By.CLASS_NAME, classStr))
          try: 
            compEle = compTableEle.find_element(By.XPATH, ".//*[contains(text(),'%s')]" % scaleHostIP)
            compParentEle = compEle.find_element(By.XPATH, "../..").find_element(By.NAME, opBtnName)
            return compParentEle
          except:
            return None
          
        # 展开需要删除的组件
        topoExpandComsArr = ['TiKV', 'TiDB', 'PD', 'TiFlash']
        
        for topoExpandCom in topoExpandComsArr:
          try: 
            compExpandEle = webWaitEle(self, (By.NAME, '%s_plus' % topoExpandCom))
            compExpandEle.click()
            sleep(2)
          except:
            pass
        
          
        # 找到目标组件 删除操作
        topoDeleteComsArr = ['tikv', 'tidb', 'pd', 'tiflash']
        for topoDeleteCom in topoDeleteComsArr:
          try: 
            compEle = findScaleInClusterEle(self, topoDeleteCom, 'deleteTopoNodeBtn')
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
        
        # 退出登录
        webWaitEle(self, (By.CLASS_NAME, 'antd-pro-components-global-header-index-account')).click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()

        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = Test()
    case.test()

