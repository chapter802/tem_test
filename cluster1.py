from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
import random

from util import util

singleMenuNameArr = ['menu.cluster.single.overview', 'menu.cluster.single.monitor', 'menu.cluster.single.performance',
                     'menu.cluster.single.backup', 'menu.cluster.single.param', 'menu.cluster.single.topology', 'menu.cluster.single.sqleditor']

perfLastTimeArr = ['5', '15', '30', '60', '180',
                   '720', '1440', '2880', '4320', '10080']

rangeStepArr = ['5', '10', '30', '60', '120', '720', '1440']

todayDate = datetime.today().strftime('%Y-%m-%d')

shortCutDateIDs = ['1', '2', '3', '4', '5',
                   '6', '7', '8', '9', '10', '11', '12']
shortCutName = 'rangePickerShortcut{id}'

# 1:DEBUG 2:INFO 3:WARN 5 CRITICAL 6 ERROR
logLevelArr = ['1', '2', '3', '5', '6']


class TestCluster(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()

    def test(self):
        def isElementExist(self, by, value):
            try:
                self.driver.find_element(by=by, value=value)
            except NoSuchElementException as e:
                return False
            return True

        def autoPage(self):
            nextPageEl = self.driver.find_element(
                By.CLASS_NAME, 'ant-table-pagination').find_element(By.CLASS_NAME, 'ant-pagination-next')
            a = nextPageEl.get_attribute('aria-disabled')
            i = 1
            while a == 'false':
                nextPageEl.click()
                i += 1
                sleep(3)
                if i > 3:
                    break

        def selectDate(self):
            randomDate = random.choice(shortCutDateIDs)
            sleep(2)
            self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
            sleep(2)
            self.driver.find_element(
                By.NAME, shortCutName.format(id=randomDate)).click()
            sleep(2)

        def selectComp(self, compName, optionPrefix, valueArr, callback=None):
            for item in valueArr:
                self.driver.find_element(
                    By.NAME, compName).click()
                sleep(1)
                target = self.driver.find_element(
                    By.NAME, optionPrefix + item)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", target)
                target.click()
                sleep(2)
                callback and callback(self)

        def selectDatePicker(self, compName):
            datePicker = self.driver.find_element(By.NAME, compName)
            datePicker.click()
            parentEle = self.driver.find_element(By.CLASS_NAME, compName)
            dateHeader = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-header')
            prevBtn = dateHeader.find_element(
                By.CLASS_NAME, 'ant-picker-header-prev-btn')
            dateContent = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-content')
            dates = dateContent.find_elements(
                By.CLASS_NAME, 'ant-picker-cell-inner')
            randomDate = random.choice(dates)
            randomDate.click()
            sleep(2)

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
            sleep(2)

            minuteCellBox = timeColums[1]
            minuteCells = minuteCellBox.find_elements(
                By.CLASS_NAME, 'ant-picker-time-panel-cell')
            randomMinute = random.choice(minuteCells)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", randomMinute)
            randomMinute.click()
            sleep(2)

            datePickerFooter = parentEle.find_element(
                By.CLASS_NAME, 'ant-picker-footer')
            datePickerFooter.find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(3)

        def startDiaLog(self):
            self.driver.find_element(
                By.NAME, 'isBaseSwitch').click()
            sleep(2)
            if isElementExist(self, By.NAME, 'reportCompareStartTime'):
                selectDatePicker(self, 'reportCompareStartTime')

                self.driver.find_element(
                    By.NAME, 'generatePerfReportBtn').click()
                sleep(10)

        def queryLog(self):
            selectDate(self)
            performLogQuerySearchBtn = self.driver.find_element(
                By.NAME, 'performLogQuerySearchBtn')
            performLogQuerySearchBtn.click()
            sleep(5)

        self.driver.get('http://172.16.6.62:8080/login')
        sleep(1)
        self.driver.find_element(
            By.ID, 'userID').send_keys('selenium_test1')
        sleep(1)
        self.driver.find_element(By.ID, 'password').send_keys('123456')
        sleep(1)
        self.driver.find_element(By.ID, 'login').click()
        sleep(2)
        self.driver.find_element(By.NAME, 'menu.cluster').click()
        sleep(3)
        activeCluster = self.driver.find_elements(
            By.CLASS_NAME, 'clusterAlias')

        if len(activeCluster) > 0:
            activeCluster[len(activeCluster) - 1].click()
        sleep(3)

        self.driver.find_element(
            By.NAME, 'menu.cluster.single.monitor').click()
        btnWrappers = self.driver.find_elements(
            By.CLASS_NAME, 'ant-radio-button-wrapper')

        for index, btnWrapper in enumerate(btnWrappers):
            btnWrapper.click()
            sleep(2)
            # if index == 2:
            #     self.driver.find_element(
            #         By.NAME, 'execInspecBtn').click()
            #     sleep(3)
            #     self.driver.find_element(
            #         By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            #     sleep(3)
        self.driver.find_element(
            By.NAME, 'menu.cluster.single.performance').click()
        sleep(2)
        # Top SQL
        # selectComp(self, 'lastTimeBox', 'last_', perfLastTimeArr)

        perfRadioBtns = self.driver.find_elements(
            By.CLASS_NAME, 'ant-radio-button-wrapper')
        perfRadioBtns[1].click()
        sleep(2)
        # 慢查询
        # selectComp(self, 'lastTimeBox', 'last_', perfLastTimeArr)
        perfRadioBtns[2].click()
        sleep(2)
        # 诊断报告
        # selectDatePicker(self, 'reportStartTime')
        # selectComp(self, 'rangeStep', 'rangeStep_', rangeStepArr, startDiaLog)
        perfRadioBtns[3].click()
        sleep(2)
        selectComp(self, 'logInfoType', 'logInfoType_', logLevelArr, queryLog)

        self.driver.find_element(
            By.NAME, 'menu.cluster.single.backup').click()
        sleep(2)
        self.driver.find_element(
            By.NAME, 'menu.cluster.single.param').click()
        sleep(2)
        autoPage(self)
        self.driver.find_element(
            By.NAME, 'menu.cluster.single.topology').click()
        sleep(2)
        self.driver.find_element(
            By.NAME, 'menu.cluster.single.sqleditor').click()
        sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    case = TestCluster()
    case.test()
