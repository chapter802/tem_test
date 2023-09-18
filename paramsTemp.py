from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

from util import util

from configParams import shortCutDateIDs, shortCutName, apiDict, paramTemplateParamType


randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryParamTemplateList', 'queryParamTemplateParams', 'createParamTemplate', 'updateParamTemplate',
             'queryParamTemplateDetail', 'deleteParamTemplate', 'applyParamTemplate', 'applyConfigCluster', 'applyClusterToParamTemplate']


class TestParamsTemp(object):
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
                sleep(3)

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

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))

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
            parentEle = self.driver.find_element(By.CLASS_NAME, compName)

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

        self.driver.get('http://172.16.6.62:8080/login')
        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['login'], closeModal)

        # 滚动到页面顶部
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)

        webWaitEle(self, (By.NAME, 'headSettingIcon')).click()
        sleep(1)
        webWaitEle(
            self, (By.CLASS_NAME, 'headerSettingDropdown')).find_element(By.NAME, 'menu.paramstemplate').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryParamTemplateList'], closeModal)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryParamTemplateParams'], closeModal)
        util.getRequsetInfo1(
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
        util.getRequsetInfo1(
            self, self.driver, apiDict['createParamTemplate'], closeModal)

        #  参数组模板详情
        paramTempNameBtns = self.driver.find_elements(
            By.NAME, 'paramTempNameBtn')
        randomparamTempNamBtn = random.choice(paramTempNameBtns)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomparamTempNamBtn)
        randomparamTempNamBtn.click()
        sleep(1)
        util.getRequsetInfo1(
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
        util.getRequsetInfo1(
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
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteParamTemplate'], closeModal)

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestParamsTemp()
    case.test()
