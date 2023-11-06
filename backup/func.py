
        # def isElementWaitExist(self, locator):
        #     try:
        #         WebDriverWait(self.driver, 20, 0.5).until(
        #             EC.visibility_of_element_located(locator))
        #         return True
        #     except:
        #         return False

        # def selectDate(self, cb=None):
        #     randomDate = random.choice(shortCutDateIDs)
        #     self.driver.find_element(By.NAME, 'rangePickerShortcut').click()
        #     webWaitEle(self, (
        #         By.NAME, shortCutName.format(id=randomDate))).click()
        #     if cb:
        #         cb(self)
        
        
         # def isElementExist(self, by, value):
        #     try:
        #         self.driver.find_element(by=by, value=value)
        #     except NoSuchElementException as e:
        #         return False
        #     return True

        # def selectComp(self, compName, optionPrefix, valueArr, callback=None):
        #     for item in valueArr:
        #         webWaitEle(self, (By.NAME, compName)).click()
        #         sleep(1)
        #         try:
        #             target = webWaitEle(self, (By.NAME, optionPrefix + item))
        #             self.driver.execute_script(
        #                 "arguments[0].scrollIntoView();", target)
        #             sleep(1)
        #             target.click()
        #         except:
        #             pass
        #         sleep(2)
        #         callback and callback(self)

        # # 开始诊断报告
        # def startDiaLog(self):
        #     self.driver.find_element(
        #         By.NAME, 'isBaseSwitch').click()
        #     sleep(2)
        #     if isElementExist(self, By.NAME, 'reportCompareStartTime'):
        #         selectTimePicker(self, 'reportCompareStartTime')
        #         self.driver.find_element(
        #             By.NAME, 'generatePerfReportBtn').click()
        #         sleep(10)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['createClusterDiagnoseReport'], closeModal)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['queryClusterDiagnoseReportStatus'], closeModal)
        #         util.getRequsetInfo(
        #             self, self.driver, apiDict['queryClusterDiagnoseReportList'], closeModal)

        # # 日志检索
        # def queryLog(self):
        #     selectDate(self)
        #     performLogQuerySearchBtn = webWaitEle(
        #         self, (By.NAME, 'performLogQuerySearchBtn'))
        #     performLogQuerySearchBtn.click()
        #     sleep(3)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchTaskID'], closeModal)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchTaskList'], closeModal)
        #     util.getRequsetInfo(
        #         self, self.driver, apiDict['queryClusterLogSearchList'], closeModal)
        #     if isElementExist(self, By.NAME, 'logDownloadShowBtn'):
        #         logDownloadShowBtn = webWaitEle(
        #             self, (By.NAME, 'logDownloadShowBtn'))
        #         logDownloadShowBtn.click()
        #         sleep(1)
        #         webWaitEle(self, (By.NAME, 'downloadLogBtn'))
        #         try:
        #             errorIconEles = self.driver.find_elements(
        #                 By.CLASS_NAME, 'anticon-close-circle')
        #             if len(errorIconEles) > 0:
        #                 webWaitEle(self, (By.NAME, 'retryLogBtn')).click()
        #                 sleep(1)
        #                 webWaitEle(self, (By.CLASS_NAME, 'ant-modal-confirm-btns')).find_element(
        #                     By.CLASS_NAME, 'ant-btn-primary').click()
        #                 sleep(1)
        #                 util.getRequsetInfo(
        #                     self, self.driver, apiDict['retryClusterLogSearchTask'], closeModal)
        #             else:
        #                 pass
        #         except:
        #             pass
        #         webWaitEle(self, (By.CLASS_NAME, 'perLogQueryDrawer')).find_element(
        #             By.CLASS_NAME, 'ant-drawer-close').click()
        #     else:
        #         pass
              
        # # 表格目标元素操作 confirmType 1: Confirm 2: popconfirm 3: direct
        # def handleTableOperation(self, targetEle, opBtnName, confirmType=3):
        #     parentEle = targetEle.find_element(By.XPATH, '..')
        #     grandParentEle = parentEle.find_element(By.XPATH, '..')
        #     targetOpBtnEle = grandParentEle.find_element(
        #         By.NAME, opBtnName)
        #     grandParentEle.find_element(By.NAME, opBtnName).click()
        #     sleep(1)
            
        #     if confirmType == 1:
        #       confirmModalEle = webWaitEle(self, (
        #         By.CLASS_NAME, 'ant-modal-confirm-body'))
        #       confirmModalEle.find_element(
        #         By.CLASS_NAME, 'ant-modal-confirm-btns').find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        #     elif confirmType == 2:
        #         webWaitEle(self, (
        #         By.CSS_SELECTOR, 'div.ant-popover-buttons > button:nth-child(2)')).click()
        #         sleep(1)
        #     elif confirmType == 3:
        #         pass
