from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import random
from util import util

from configParams import apiDict, backupDestination, backupAK, backupSK

driver = webdriver.Chrome()
driver.implicitly_wait(10)
randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryBackupTaskList', 'queryBackupTopSummary',
             'deleteBackupTask', 'backupCluster', 'restoreCluster', 'stopBackupTask', 'detectRestoreCluster', 'queryRestoreBackupList',
             'queryBackupPoliciesList', 'deleteBackupPolicy', 'createBackupPolicy', 'updateBackupPolicy', 'queryBackupPolicyDetail']


class TestBackup(object):
    def __init__(self):
        self.driver = driver
        self.logger = util.get_logger()
        self.driver.maximize_window()

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

            if notiCLoseEle != None:
                notiCLoseEle.click()
            elif drawerCusCloseBtn != None:
                drawerCusCloseBtn.click()
            elif modalCloseBtn != None:
                modalCloseBtn.click()

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))

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
        webWaitEle(self, (By.NAME, 'menu.backup')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryBackupTaskList'], closeModal)
        util.getRequsetInfo1(
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
        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['backupCluster'], closeModal)
        # 等待十秒备份
        sleep(10)

        # 删除备份任务
        backupDeleteBtns = self.driver.find_elements(
            By.NAME, 'backupDeleteBtn')
        if len(backupDeleteBtns) > 0:
            firstDeleteBtn = backupDeleteBtns[0]
            firstDeleteBtn.click()

            confirmTagetVal = webWaitEle(
                self, (By.ID, 'TaskID')).get_attribute('data-tval')
            webWaitEle(self, (By.ID, 'TaskID')).send_keys(confirmTagetVal)
            webWaitEle(self, (By.CLASS_NAME, 'confirmDeleteModal')).find_element(
                By.CLASS_NAME, 'ant-btn-danger').click()
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteBackupTask'], closeModal)
        else:
            pass

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
                    print(len(backupNameEles))
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
            util.getRequsetInfo1(
                self, self.driver, apiDict['detectRestoreCluster'], closeModal)
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            util.getRequsetInfo1(
                self, self.driver, apiDict['restoreCluster'], closeModal)
        else:
            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-default').click()

        # 管理备份策略
        webWaitEle(self, (By.NAME, 'policyBtn')).click()
        sleep(1)
        util.getRequsetInfo1(
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
        applyClusterEles = webWaitEle(self, (By.CLASS_NAME, 'backupModalClusterIDsSelect')).find_elements(
            By.CLASS_NAME, 'ant-select-item-option')
        if len(applyClusterEles) > 0:
            random.choice(applyClusterEles).click()
        else:
            pass

        backupPolicyWeekEle = webWaitEle(self, (By.ID, 'week'))
        if backupPolicyWeekEle:
            randomDays = random.sample(range(1, 8), random.randint(1, 7))
            weekdayEles = backupPolicyWeekEle.find_elements(
                By.CLASS_NAME, 'ant-checkbox-wrapper')
            for day in randomDays:
                weekdayEles[day-1].click()
        else:
            pass

        selectTimePicker(self, 'backupPolicyModalTimepicker')
        webWaitEle(self, (By.ID, 'Retention')).send_keys(
            random.randint(1, 365))

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-primary').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['createBackupPolicy'], closeModal)

        # 编辑备份策略
        webWaitEle(self, (By.NAME, 'backupPolicyEditBtn'))
        editBtns = self.driver.find_elements(
            By.NAME, 'backupPolicyEditBtn')
        if len(editBtns) > 0:
            lastEditBtn = editBtns[-1]
            lastEditBtn.click()
            policyNameEle = webWaitEle(self, (By.ID, 'Name'))
            util.clearInput(policyNameEle)
            policyNameEle.send_keys('selenium_policy' + randomStr + '_edit')
            backupDestinationEle = webWaitEle(self, (By.ID, 'Destination'))
            util.clearInput(backupDestinationEle)
            backupDestinationEle.send_keys(backupDestination.format(randomStr))

            backupPolicyWeekEle = webWaitEle(self, (By.ID, 'week'))
            if backupPolicyWeekEle:
                randomDays = random.sample(range(1, 8), random.randint(1, 7))
                weekdayEles = backupPolicyWeekEle.find_elements(
                    By.CLASS_NAME, 'ant-checkbox-wrapper')
                for day in randomDays:
                    weekdayEles[day-1].click()
            else:
                pass
            selectTimePicker(self, 'backupPolicyModalTimepicker')
            webWaitEle(self, (By.ID, 'Retention')).send_keys(
                random.randint(1, 365))

            webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
                By.CLASS_NAME, 'ant-btn-primary').click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['updateBackupPolicy'], closeModal)

        else:
            pass

        sleep(3)

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
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteBackupPolicy'], closeModal)

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestBackup()
    case.test()
