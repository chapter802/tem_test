from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

from util import util

from configParams import shortCutDateIDs, shortCutName, apiDict


randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryInspecPolicyList', 'queryInspections', 'clusterList', 'createInspecPolicy',
             'updateInspecPolicy', 'queryInspecPolicyDetail', 'deleteInspection', 'createInspection', 'deleteInspecPolicy']


class TestInspection(object):
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
            self, (By.CLASS_NAME, 'headerSettingDropdown')).find_element(By.NAME, 'menu.inspection').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryInspecPolicyList'], closeModal)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryInspections'], closeModal)
        util.getRequsetInfo1(
            self, self.driver, apiDict['clusterList'], closeModal)
        self.driver.find_element(By.TAG_NAME, 'body').click()
        sleep(1)

        # # 创建巡检策略
        # webWaitEle(self, (By.NAME, 'addInspectionPolicyBtn')).click()
        # webWaitEle(self, (By.ID, 'Alias')).send_keys(
        #     'selenium_test_' + randomStr)
        # webWaitEle(self, (By.NAME, 'inspecPolicySwitch')).click()
        # webWaitEle(self, (By.ID, 'Description')).send_keys(
        #     'selenium_Description_' + randomStr)

        # inpecPolicyWeekEle = webWaitEle(self, (By.ID, 'FrequencyWeek'))
        # if inpecPolicyWeekEle:
        #     randomDays = random.sample(range(1, 8), random.randint(1, 7))
        #     weekdayEles = inpecPolicyWeekEle.find_elements(
        #         By.CLASS_NAME, 'ant-checkbox-wrapper')
        #     for day in randomDays:
        #         weekdayEles[day-1].click()
        # else:
        #     pass

        # selectTimePicker(self, 'inspecPolicyModalTimepicker')

        # webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
        #     By.CLASS_NAME, 'ant-btn-primary').click()
        # sleep(1)
        # util.getRequsetInfo1(
        #     self, self.driver, apiDict['createInspecPolicy'], closeModal)

        # #  巡检策略详情
        # inspecPolicyAliasBtns = self.driver.find_elements(
        #     By.NAME, 'inspecPolicyAliasBtn')
        # randomPolicyAliasBtn = random.choice(inspecPolicyAliasBtns)
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", randomPolicyAliasBtn)
        # randomPolicyAliasBtn.click()
        # sleep(1)
        # util.getRequsetInfo1(
        #     self, self.driver, apiDict['queryInspecPolicyDetail'], closeModal)
        # webWaitEle(self, (By.CLASS_NAME, 'ant-drawer-close')).click()

        # # 编辑巡检策略
        # updateInspectionPolicyBtns = self.driver.find_elements(
        #     By.NAME, 'updateInspectionPolicyBtn')
        # lastUpdateInspectionPolicyBtn = updateInspectionPolicyBtns[-1]
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", lastUpdateInspectionPolicyBtn)
        # sleep(1)
        # lastUpdateInspectionPolicyBtn.click()
        # sleep(1)
        # inpspecModalAlias = webWaitEle(self, (By.ID, 'Alias'))
        # util.clearInput(inpspecModalAlias)
        # inpspecModalAlias.send_keys('selenium_test_' + randomStr)
        # webWaitEle(self, (By.NAME, 'inspecPolicySwitch')).click()
        # inpspecModalDesc = webWaitEle(self, (By.ID, 'Description'))
        # util.clearInput(inpspecModalDesc)
        # inpspecModalDesc.send_keys('selenium_Description_' + randomStr)

        # inpecPolicyWeekEle = webWaitEle(self, (By.ID, 'FrequencyWeek'))
        # if inpecPolicyWeekEle:
        #     randomDays = random.sample(range(1, 8), random.randint(1, 7))
        #     weekdayEles = inpecPolicyWeekEle.find_elements(
        #         By.CLASS_NAME, 'ant-checkbox-wrapper')
        #     for day in randomDays:
        #         weekdayEles[day-1].click()
        # else:
        #     pass

        # selectTimePicker(self, 'inspecPolicyModalTimepicker')

        # webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
        #     By.CLASS_NAME, 'ant-btn-primary').click()
        # sleep(1)
        # util.getRequsetInfo1(
        #     self, self.driver, apiDict['updateInspecPolicy'], closeModal)

        # 应用集群
        applyClusterBtns = self.driver.find_elements(
            By.NAME, 'applyClusterBtn')
        # lastApplyClusterBtn = applyClusterBtns[-1]
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", lastApplyClusterBtn)
        # sleep(1)
        # lastApplyClusterBtn.click()
        firstApplyClusterBtn = applyClusterBtns[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", firstApplyClusterBtn)
        sleep(1)
        firstApplyClusterBtn.click()
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
        util.getRequsetInfo1(
            self, self.driver, apiDict['createInspection'], closeModal)
        util.getRequsetInfo1(
            self, self.driver, apiDict['deleteInspection'], closeModal)

        # 删除巡检策略
        deleteInspectionPolicyBtns = self.driver.find_elements(
            By.NAME, 'deleteInspectionPolicyBtn')
        lastDeleteInspectionPolicyBtn = deleteInspectionPolicyBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastDeleteInspectionPolicyBtn)
        sleep(1)
        if lastDeleteInspectionPolicyBtn:
            lastDeleteInspectionPolicyBtn.click()
            sleep(1)
        inpecApplyClustersEles = self.driver.find_elements(
            By.NAME, 'inpecApplyClusters')
        lastInpecApplyClustersEle = inpecApplyClustersEles[-1]
        lastInpecApplyClustersEleText = util.getElementText(
            self, lastInpecApplyClustersEle)

        if lastInpecApplyClustersEleText == '':
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.inspectionDeletePopconfirm  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteInspecPolicy'], closeModal)

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestInspection()
    case.test()
