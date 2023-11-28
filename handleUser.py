# 2.1.0
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

from util import util

from configParams import shortCutDateIDs, shortCutName, apiDict, userPwd, testServer


randomStr = util.get_random_string(6)

# 测试用例中的接口
apiKeyArr = ['queryParamTemplateList', 'queryParamTemplateParams', 'createParamTemplate', 'updateParamTemplate',
             'queryParamTemplateDetail', 'deleteParamTemplate', 'applyParamTemplate', 'applyConfigCluster', 'applyClusterToParamTemplate']

# 集群管理列表页请求的接口
mainPageApiArr = ['clusterList', 'clusterTops', 'clusterTopAlert',
                  'clusterPerfSummary', 'clusterAlertSummary', 'queryClusterMonitorInfo']


class TestParamsTemp(object):
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

            if notiCLoseEle != None:
                notiCLoseEle.click()
            elif drawerCusCloseBtn != None:
                drawerCusCloseBtn.click()
            elif modalCloseBtn != None:
                modalCloseBtn.click()

        def webWaitEle(self, locator):
            return WebDriverWait(self.driver, 20, 0.5).until(
                EC.visibility_of_element_located(locator))
            
        # 滑动到顶部
        def scrollToTop(self):
            js = "var q=document.documentElement.scrollTop=0"
            self.driver.execute_script(js)
            sleep(2)
        
        # 登录    
        def login(self, server, userName, password):
            self.driver.get(server)
            webWaitEle(self, (By.ID, 'userID')).send_keys(userName)
            webWaitEle(self, (By.ID, 'password')).send_keys(password)
            webWaitEle(self, (By.ID, 'login')).click()
            sleep(1)
            util.getRequsetInfo(
                self, self.driver, apiDict['login'], closeModal)
        
        # 进入用户管理页面
        def goToUserPage(self):
          # 滚动到页面顶部
          scrollToTop(self)

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
        def createUser(self, userName, authIndex):
          # 滚动到页面顶部
          scrollToTop(self)
          # authIndex 0 全部权限 1:管理员权限 2:ALERT_MANAGER 3:ALERT_READER 4:BACKUP_MANAGER 5:BACKUP_READER 6:CLUSTER_MANAGER 7:CLUSTER_READER 8:HOST_MANAGER 9:HOST_READER 10:USER_MANAGER 11:AUDIT_MANAGER
          webWaitEle(self, (By.NAME, 'addUserBtn')).click()
          userModalEle = webWaitEle(self, (By.CLASS_NAME, 'updateUserInfoModal'))
          webWaitEle(self, (By.ID, 'UserID')).send_keys(userName)
          webWaitEle(self, (By.ID, 'Password')).send_keys(userPwd)
          # 选中权限
          authCheckEles = userModalEle.find_elements(By.CLASS_NAME, 'ant-checkbox-wrapper')
          adminAuthCheckEle = authCheckEles[authIndex]
          adminAuthCheckEle.click()
          sleep(1)
          userModalEle.find_element(By.CLASS_NAME, 'ant-modal-footer').find_element(
              By.CLASS_NAME, 'ant-btn-primary').click()
          # 进入预览信息页面再次确认
          sleep(1)
          userModalEle.find_element(By.CLASS_NAME, 'ant-modal-footer').find_element(
              By.CLASS_NAME, 'ant-btn-primary').click()
          sleep(2)
          util.getRequsetInfo(
            self, self.driver, apiDict['userAdd'], closeModal)
          sleep(2)
          # 报错处理, 用户已存在 需要二次取消关闭
          closeModal(self)
          
          sleep(1)
          # 退出登录
          logout(self)
         
        # 退出登录 
        def logout(self):
          webWaitEle(self, (By.CLASS_NAME, 'antd-pro-components-global-header-index-account')).click()
          sleep(1)
          webWaitEle(self, (By.CLASS_NAME, 'anticon-logout')).click()
          util.getRequsetInfo(
            self, self.driver, apiDict['logout'], closeModal)
          
        # 删除测试用户
        def deleteUser(self, userName):
          # 登录 user_test 用户
          login(self, testServer, 'user_test', userPwd)
          
          # 进入用户管理页面
          goToUserPage(self)
          
          # 分页调到最大页
          webWaitEle(self, (By.CLASS_NAME, 'ant-pagination-options-size-changer')).click()
          paginationOptions = webWaitEle(self, (By.CLASS_NAME, 'rc-virtual-list')).find_elements(By.CLASS_NAME, 'ant-select-item-option')
          lastPaginationOption = paginationOptions[-1]
          lastPaginationOption.click()
          sleep(1)
          util.getRequsetInfo(
            self, self.driver, apiDict['userList'], closeModal)
          sleep(1)
          
          # 找到测试的目标用户
          targetUserTextEle = webWaitEle(
          self, (By.XPATH, "//*[contains(text(), '{}')]".format(userName)))
          self.driver.execute_script(
                "arguments[0].scrollIntoView();", targetUserTextEle)
          sleep(1)
          targetTrEle = targetUserTextEle.find_element(
              By.XPATH, '../..')
          deleteUserBtn = targetTrEle.find_element(
              By.NAME, 'deleteUserBtn')
          deleteUserBtn.click()
          
          deleteUserConfirmModal = webWaitEle(self, (By.CLASS_NAME, 'deleteUserConfirm'))
          # 确认删除
          deleteUserConfirmModal.find_element(By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(
              By.CLASS_NAME, 'ant-btn-primary').click()
          sleep(1)
          util.getRequsetInfo(
            self, self.driver, apiDict['deleteUser'], closeModal)
          sleep(2)

        # 登录
        login(self, testServer, 'selenium_test', userPwd)
        
        # 进入用户管理页面
        goToUserPage(self)

        # 创建 user_test 用户
        createUser(self, 'user_test', 1)
        
        # 登录 user_test 用户 创建 user_test_1 用户
        login(self, testServer, 'user_test', userPwd)
        
        # 进入用户管理页面
        goToUserPage(self)
        
        # 创建 user_test_1 用户 权限用户管理权限
        createUser(self, 'user_test_1', 10)
        
        #登录 user_test_1 用户 检查用户管理权限
        login(self, testServer, 'user_test_1', userPwd)
        
        # 进入用户管理页面      ---> 待补充权限自定义校验日志
        goToUserPage(self)
        
         # 退出登录
        logout(self)
        
        # 删除 user_test_1 用户
        deleteUser(self, 'user_test_1')
        
        # 创建 user_test2 用户 cluster manager 角色
        createUser(self, 'user_test2', 6)
        
        login(self, testServer, 'user_test2', userPwd)
        
        try:
          # 跳转到集群列表页面
          webWaitEle(self, (By.NAME, 'menu.cluster')).click()
          sleep(2)
          for api in mainPageApiArr:
              util.getRequsetInfo(
                  self, self.driver, apiDict[api], closeModal)
          sleep(1)
          self.logger.info('user_test2 用户有集群管理所有权限')
        except:
          self.logger.error('user_test2 用户没有集群管理权限')
          
        # 退出登录
        logout(self)
          
        # 登录 user_test 用户 删除 user_test2 用户
        deleteUser(self, 'user_test2')
        
        # 创建 user_test3 用户 cluster reader 角色
        createUser(self, 'user_test3', 7)
        
        # 登录 user_test3 用户 检查集群管理权限
        login(self, testServer, 'user_test3', userPwd)
        
        try:
          # 跳转到集群列表页面
          webWaitEle(self, (By.NAME, 'menu.cluster')).click()
          sleep(2)
          for api in mainPageApiArr:
              util.getRequsetInfo(
                  self, self.driver, apiDict[api], closeModal)
          sleep(1)
          self.logger.info('user_test3 用户有集群管理只读权限')
        except:
          self.logger.error('user_test3 用户没有集群管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test3 用户
        deleteUser(self, 'user_test3')
        
        # 创建 user_test4 用户 alert manager 角色
        createUser(self, 'user_test4', 2)
        
        # 登录 user_test4 用户 检查告警管理权限
        login(self, testServer, 'user_test4', userPwd)
        
        try:
          # 跳转到告警管理 - 告警规则页面
          webWaitEle(self, (By.NAME, 'menu.alert')).click()
          webWaitEle(self, (By.NAME, 'menu.alert.rules')).click()
          sleep(1)
          util.getRequsetInfo(
              self, self.driver, apiDict['queryAlertRuleIndicators'], closeModal)
          sleep(1)
          webWaitEle(self, (By.NAME, 'alertRulesAddBtn'))
          self.logger.info('user_test4 用户有告警管理权限')
        except:
          self.logger.error('user_test4 用户没有告警管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test4 用户
        deleteUser(self, 'user_test4')
        
        # 创建 user_test5 用户 alert reader 角色
        createUser(self, 'user_test5', 3)
        
        # 登录 user_test5 用户 检查告警管理权限
        login(self, testServer, 'user_test5', userPwd)
        
        try:
          # 跳转到告警管理 - 告警事件页面
          webWaitEle(self, (By.NAME, 'menu.alert')).click()
          webWaitEle(self, (By.NAME, 'menu.alert.event')).click()
          sleep(1)
          util.getRequsetInfo(
              self, self.driver, apiDict['queryAlertEventList'], closeModal)
          sleep(1)
          self.logger.info('user_test5 用户有告警管理只读权限')
        except:
          self.logger.error('user_test5 用户没有告警管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test5 用户
        deleteUser(self, 'user_test5')
        
        # 创建 user_test6 用户 backup manager 角色
        createUser(self, 'user_test6', 4)
        
        # 登录 user_test6 用户 检查备份管理权限
        login(self, testServer, 'user_test6', userPwd)
        
        try:
          # 跳转到备份管理页面
          webWaitEle(self, (By.NAME, 'menu.backup')).click()
          sleep(1)
          util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTaskList'], closeModal)
          util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTopSummary'], closeModal)
          sleep(1)
          webWaitEle(self, (By.NAME, 'manualBackupBtn'))
          self.logger.info('user_test6 用户有备份管理权限')
        except:
          self.logger.error('user_test6 用户没有备份管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test6 用户  
        deleteUser(self, 'user_test6')
        
        # 创建 user_test7 用户 backup reader 角色
        createUser(self, 'user_test7', 5)
        
        # 登录 user_test7 用户 检查备份管理权限
        login(self, testServer, 'user_test7', userPwd)
        
        try:
          # 跳转到备份管理页面
          webWaitEle(self, (By.NAME, 'menu.backup')).click()
          sleep(1)
          util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTaskList'], closeModal)
          util.getRequsetInfo(
            self, self.driver, apiDict['queryBackupTopSummary'], closeModal)
          sleep(1)
          self.logger.info('user_test7 用户有备份管理只读权限')
        except:
          self.logger.error('user_test7 用户没有备份管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test7 用户
        deleteUser(self, 'user_test7')
        
        # 创建 user_test8 用户 host manager 角色
        createUser(self, 'user_test8', 8)
        
        # 登录 user_test8 用户 检查主机管理权限
        login(self, testServer, 'user_test8', userPwd)
        
        try:
          # 跳转到主机管理页面
          webWaitEle(self, (By.NAME, 'menu.host')).click()
          sleep(1)
          util.getRequsetInfo(
              self, self.driver, apiDict['queryHostList'], closeModal)
          sleep(1)
          webWaitEle(self, (By.NAME, 'createHostBtn'))
          self.logger.info('user_test8 用户有主机管理权限')
        except:
          self.logger.error('user_test8 用户没有主机管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test8 用户
        deleteUser(self, 'user_test8')
        
        # 创建 user_test9 用户 host reader 角色
        createUser(self, 'user_test9', 9)
        
        # 登录 user_test9 用户 检查主机管理权限
        login(self, testServer, 'user_test9', userPwd)
        
        try:
          # 跳转到主机管理页面
          webWaitEle(self, (By.NAME, 'menu.host')).click()
          sleep(1)
          util.getRequsetInfo(
              self, self.driver, apiDict['queryHostList'], closeModal)
          sleep(1)
          self.logger.info('user_test9 用户有主机管理只读权限')
        except:
          self.logger.error('user_test9 用户没有主机管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test9 用户
        deleteUser(self, 'user_test9')
        
        # 创建 user_test10 用户 audit manager 角色
        createUser(self, 'user_test10', 11)
        
        # 登录 user_test10 用户 检查审计管理权限
        login(self, testServer, 'user_test10', userPwd)
        
        try:
          # 跳转到审计管理页面
          webWaitEle(self, (By.NAME, 'menu.audit')).click()
          sleep(1)
          util.getRequsetInfo(
              self, self.driver, apiDict['queryAuditList'], closeModal)
          sleep(1)
          self.logger.info('user_test10 用户有审计管理权限')
        except:
          self.logger.error('user_test10 用户没有审计管理权限')
          
        # 退出登录
        logout(self)
        
        # 登录 user_test 用户 删除 user_test10 用户
        deleteUser(self, 'user_test10')
        
        sleep(5)
        
        # 退出登录
        logout(self)
        
        sleep(5)

        self.driver.quit()


if __name__ == '__main__':
    case = TestParamsTemp()
    case.test()
