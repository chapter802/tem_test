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
apiKeyArr = ['userList', 'userAdd', 'userEdit',
             'roleList', 'deleteUser', 'changeUserPwd']


class TestUserManage(object):
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
        util.getRequsetInfo(
            self, self.driver, apiDict['login'], closeModal)

        # 滚动到页面顶部
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)

        webWaitEle(self, (By.NAME, 'headSettingIcon')).click()
        sleep(1)
        webWaitEle(
            self, (By.CLASS_NAME, 'headerSettingDropdown')).find_element(By.NAME, 'menu.usermanage').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['userList'], closeModal)
        util.getRequsetInfo(
            self, self.driver, apiDict['roleList'], closeModal)
        self.driver.find_element(By.TAG_NAME, 'body').click()
        sleep(1)

        # 创建用户
        webWaitEle(self, (By.NAME, 'addUserBtn')).click()
        webWaitEle(self, (By.ID, 'UserID')).send_keys(
            'selenium_test_' + randomStr)
        webWaitEle(self, (By.ID, 'Password')).send_keys('tem')
        webWaitEle(self, (By.ID, 'Phone')).send_keys('18567618191')
        webWaitEle(self, (By.ID, 'Note')).send_keys(
            'selenium_Note_' + randomStr)
        userCheckWrapperEles = self.driver.find_elements(
            By.CLASS_NAME, 'ant-checkbox-wrapper')
        randomCheckWrapperEle = random.choice(userCheckWrapperEles)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomCheckWrapperEle)
        sleep(1)
        randomCheckWrapperEle.click()
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['userAdd'], closeModal)

        autoPage(self)

        # 编辑用户
        updateUserBtns = self.driver.find_elements(
            By.NAME, 'updateUserBtn')
        lastUpdateUserBtn = updateUserBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastUpdateUserBtn)
        sleep(1)
        lastUpdateUserBtn.click()
        sleep(1)
        userModalDesc = webWaitEle(self, (By.ID, 'Note'))
        util.clearInput(userModalDesc)
        userModalDesc.send_keys('selenium_Note_' + randomStr)
        userCheckWrapperEles = self.driver.find_elements(
            By.CLASS_NAME, 'ant-checkbox-wrapper')
        randomCheckWrapperEle = random.choice(userCheckWrapperEles)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", randomCheckWrapperEle)
        sleep(1)
        randomCheckWrapperEle.click()
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo(
            self, self.driver, apiDict['userEdit'], closeModal)

        # 修改密码
        changeUserPwdBtns = self.driver.find_elements(
            By.NAME, 'changeUserPwdBtn')
        lastChangeUserPwdBtn = changeUserPwdBtns[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastChangeUserPwdBtn)
        sleep(1)
        lastChangeUserPwdBtn.click()
        webWaitEle(self, (By.ID, 'NewPassword')).send_keys('123456')
        webWaitEle(self, (By.ID, 'ConfirmNewPassword')).send_keys('123456')
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(2)
        util.getRequsetInfo(
            self, self.driver, apiDict['changeUserPwd'], closeModal)

        # 删除用户
        autoPage(self)
        deleteUserBtn = self.driver.find_elements(
            By.NAME, 'deleteUserBtn')
        lastDeleteUserBtn = deleteUserBtn[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", lastDeleteUserBtn)
        sleep(1)
        if lastDeleteUserBtn:
            lastDeleteUserBtn.click()
            sleep(1)
            webWaitEle(self, (
                By.CSS_SELECTOR, 'div.ant-modal-confirm-btns  button:nth-child(2)')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['deleteUser'], closeModal)

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestUserManage()
    case.test()
