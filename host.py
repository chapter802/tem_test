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
apiKeyArr = ['queryHostList', 'discoverHost', 'createHost', 'updateHost', 'deleteHost',
             'queryHostMonitor', 'queryHostOption', 'querySpecList', 'createSpec', 'updateSpec', 'deleteSpec',
             'queryAuditLogOption', 'queryAuditLog',  # 审计日志
             'queryTaskFlowList', 'queryTaskFlowDetail']  # 任务流


class TestHost(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = util.get_logger()
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

        self.driver.get('http://172.16.6.62:8080/login')
        webWaitEle(self, (By.ID, 'userID')).send_keys('selenium_test1')
        webWaitEle(self, (By.ID, 'password')).send_keys('123456')
        webWaitEle(self, (By.ID, 'login')).click()
        webWaitEle(self, (By.NAME, 'menu.host')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryHostList'], closeModal)

        # 创建主机和主机规格
        webWaitEle(self, (By.NAME, 'createHostBtn')).click()
        webWaitEle(self, (By.ID, 'IP')).send_keys('172.17.0.5')
        webWaitEle(self, (By.ID, 'UserName')).send_keys('root')
        webWaitEle(self, (By.ID, 'Password')).send_keys('tem')
        webWaitEle(self, (By.ID, 'SSHPort')).send_keys('22')
        webWaitEle(self, (By.NAME, 'hostModalFindBtn')).click()
        util.getRequsetInfo1(
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
                sleep(1)
                util.getRequsetInfo1(
                    self, self.driver, apiDict['createSpec'], closeModal)

        saveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')
                                 ).find_element(By.CLASS_NAME, 'ant-btn-primary')
        if saveHostBtn.get_attribute('disabled'):
            return
        else:
            saveHostBtn.click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['createHost'], closeModal)
        sleep(1)

        # 编辑主机
        testHostEle = webWaitEle(
            self, (By.XPATH, "//*[contains(text(), '172.17.0.5')]"))
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
        util.getRequsetInfo1(
            self, self.driver, apiDict['discoverHost'], closeModal)
        saveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')
                                 ).find_element(By.CLASS_NAME, 'ant-btn-primary')
        if saveHostBtn.get_attribute('disabled'):
            return
        else:
            saveHostBtn.click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['createHost'], closeModal)
        sleep(1)

        # 主机详情
        testHostEle.click()
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryHostMonitor'], closeModal)
        sleep(1)
        hostDetailCloseBtn = webWaitEle(self, (
            By.CLASS_NAME, 'ant-modal-content')).find_element(By.CLASS_NAME, 'ant-modal-close')
        hostDetailCloseBtn.click()
        sleep(1)
        # 下线主机
        parentEle = testHostEle.find_element(By.XPATH, '..')
        grandParentEle = parentEle.find_element(By.XPATH, '..')
        grandParentEle.find_element(By.NAME, 'hostOfflineBtn').click()
        confirmHostTagetVal = webWaitEle(
            self, (By.ID, 'IP')).get_attribute('data-tval')
        webWaitEle(self, (By.ID, 'IP')).send_keys(confirmHostTagetVal)

        webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')).find_element(
            By.CLASS_NAME, 'ant-btn-danger').click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['deleteHost'], closeModal)
        # 下线主机等待60s
        sleep(60)

        # 批量添加主机
        webWaitEle(self, (By.NAME, 'batchAddHostBtn')).click()
        webWaitEle(self, (By.ID, 'UserName')).send_keys('root')
        webWaitEle(self, (By.ID, 'Password')).send_keys('tem')
        webWaitEle(self, (By.ID, 'SSHPort')).send_keys('22')
        webWaitEle(self, (By.ID, 'HostList')).send_keys('172.17.0.5')
        webWaitEle(self, (By.NAME, 'batchAddHostTestBtn')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['discoverHost'], closeModal)

        batchSaveHostBtn = webWaitEle(self, (By.CLASS_NAME, 'ant-modal-footer')
                                      ).find_element(By.CLASS_NAME, 'ant-btn-primary')
        if batchSaveHostBtn.get_attribute('disabled'):
            return
        else:
            batchSaveHostBtn.click()
            sleep(1)
            util.getRequsetInfo1(
                self, self.driver, apiDict['createHost'], closeModal)
        sleep(1)

        # 主机规格管理
        self.driver.find_element(By.NAME, 'hostSpecManageBtn').click()
        sleep(1)
        util.getRequsetInfo1(
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
                util.getRequsetInfo1(
                    self, self.driver, apiDict['createSpec'], closeModal)
            else:
                util.getRequsetInfo1(
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
            util.getRequsetInfo1(
                self, self.driver, apiDict['deleteSpec'], closeModal)

        # 审计日志
        webWaitEle(self, (By.NAME, 'menu.audit.log')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryAuditLogOption'], closeModal)

        selectDate(self)
        webWaitEle(self, (By.NAME, 'auditLogSearchBtn')).click()
        sleep(1)
        util.getRequsetInfo1(
            self, self.driver, apiDict['queryAuditLog'], closeModal)

        # 任务流
        webWaitEle(self, (By.NAME, 'menu.taskflow')).click()
        sleep(1)
        util.getRequsetInfo1(
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
            util.getRequsetInfo1(
                self, self.driver, apiDict['queryTaskFlowDetail'], closeModal)
            sleep(1)
            taskflowDetailCloseBtn = webWaitEle(self, (
                By.CLASS_NAME, 'ant-modal-content')).find_element(By.CLASS_NAME, 'ant-modal-close')
            taskflowDetailCloseBtn.click()
            sleep(1)

        # 滚动到页面顶部
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + Keys.HOME)

        webWaitEle(self, (By.NAME, 'headSettingIcon')).click()

        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestHost()
    case.test()
