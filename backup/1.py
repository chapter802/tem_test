from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import platform
import pickle
import random
import string
import json
import gzip
from configParams import apiDict


def get_logger():
    import logging
    import logging.handlers
    import datetime
    import os

    def contains_folder(path, folder_name):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and item == folder_name:
                return True
        return False

    def create_folder(path, folder_name):
        folder_path = os.path.join(path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    cwd = os.getcwd()
    temTestPath = cwd + '/tem_test'

    if contains_folder(temTestPath, "Logs") == False:
        create_folder(temTestPath, "Logs")

    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler(temTestPath + '/Logs/all.log', when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler(temTestPath + '/Logs/error.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger


# 生成随机字符串
def gen_random_str():
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies, filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def clearInput(element):
    controlKey = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
    element.send_keys(controlKey + "a")
    element.send_keys(Keys.DELETE)
    sleep(1)


def generateIpAddress():
    ip_address = []
    for i in range(4):
        ip_address.append(str(random.randint(0, 255)))
    return ".".join(ip_address)


def contains_all_words(string_array, test_string):
    for word in string_array:
        if word not in test_string:
            return False
    return True


def getRequsetInfo(self, requests, curUrl, actionText, reqMethod='POST', excludeStr='', errCb=None):
    upCaseMethod = reqMethod.upper()
    reverseRequests = requests[::-1]
    for request in reverseRequests:
        if request.response:
            if curUrl in request.url and upCaseMethod in request.method:
                if (excludeStr != '' and excludeStr not in request.url) | (excludeStr == ''):
                    _method = request.method
                    _status = request.response.status_code
                    _params = request.body.decode('utf-8')
                    _apiUrl = request.url
                    _content = request.response.body
                    try:
                        _content = gzip.decompress(request.response.body)
                    except:
                        _content = request.response.body
                    # _content = request.response.body

                    # 获取接口返回内容
                    try:
                        _sucessContent = _content.decode('utf-8')
                        jsonContent = json.loads(_sucessContent)
                        if (jsonContent['Success'] != True):
                            self.logger.error(
                                actionText + '失败: \n Request URL: {a} \n Request Method: {me} \n RequsetParams: {p} \n Status Code: {s} \n Code: {c} \n Message: {m}'.format(a=_apiUrl, me=_method, p=_params, s=_status, c=jsonContent['Code'], m=jsonContent['Message']))
                            self.driver.save_screenshot(actionText + '失败.png')
                            errCb and errCb(self)
                        else:
                            self.logger.debug(
                                actionText + '成功: \n Request URL: {a} \n Request Method: {me}'.format(a=_apiUrl, me=_method))
                        return jsonContent
                    except:
                        return _content


def getRequsetInfo(self, driver, apiConfig, errCb=None):
    requests = driver.requests
    upCaseMethod = apiConfig['method']
    actionText = apiConfig['remark']
    excludeStr = apiConfig['excludeStr']
    reverseRequests = requests[::-1]

    for request in reverseRequests:
        if request.response:
            urlStrs = apiConfig['urlStrs']
            iscontainAll = contains_all_words(urlStrs, request.url)
            if iscontainAll and upCaseMethod in request.method:
                # print('request.url----', request.url)
                if (excludeStr != '' and excludeStr not in request.url) | (excludeStr == ''):
                    _method = request.method
                    _status = request.response.status_code
                    _params = request.body.decode('utf-8')
                    _apiUrl = request.url
                    _content = request.response.body
                    try:
                        _content = gzip.decompress(request.response.body)
                    except:
                        _content = request.response.body
                    # _content = request.response.body

                    # 获取接口返回内容
                    try:
                        _sucessContent = _content.decode('utf-8')
                        jsonContent = json.loads(_sucessContent)
                        if (jsonContent['Success'] != True):
                            self.logger.error(
                                actionText + '失败: \n Request URL: {a} \n Request Method: {me} \n RequsetParams: {p} \n Status Code: {s} \n Code: {c} \n Message: {m}'.format(a=_apiUrl, me=_method, p=_params, s=_status, c=jsonContent['Code'], m=jsonContent['Message']))
                            self.driver.save_screenshot(actionText + '失败.png')
                            errCb and errCb(self)
                        else:
                            self.logger.debug(
                                actionText + '成功: \n Request URL: {a} \n Request Method: {me}'.format(a=_apiUrl, me=_method))
                        return jsonContent
                    except:
                        return _content


def getSingleRequsetInfo(self, request, curUrl, actionText, reqMethod='POST', excludeStr='', errCb=None):
    upCaseMethod = reqMethod.upper()

    if request.response:

        if curUrl in request.url and upCaseMethod in request.method:
            if (excludeStr != '' and excludeStr not in request.url) | (excludeStr == ''):
                _method = request.method
                _status = request.response.status_code
                _params = request.body.decode('utf-8')
                _apiUrl = request.url
                # _content = gzip.decompress(request.response.body)
                _content = request.response.body
                print('jsonContent----', _content.decode('utf-8'))
                # 获取接口返回内容
                try:
                    _sucessContent = _content.decode('utf-8')
                    jsonContent = json.loads(_sucessContent)
                    if (jsonContent['Success'] != True):
                        self.logger.error(
                            actionText + '失败: \n Request URL: {a} \n Request Method: {me} \n RequsetParams: {p} \n Status Code: {s} \n Code: {c} \n Message: {m}'.format(a=_apiUrl, me=_method, p=_params, s=_status, c=jsonContent['Code'], m=jsonContent['Message']))
                        errCb and errCb(self)
                    else:
                        self.logger.debug(
                            actionText + '成功: \n Request URL: {a} \n Request Method: {me}'.format(a=_apiUrl, me=_method))
                    return jsonContent
                except:
                    return _content
    sleep(1)


def getAllReqInfo(self, requests, apiKeys, errCb=None):
    if apiKeys and len(apiKeys) > 0:

        def findApiRequest(_urlStrs, _configMethod, _excludeStr):
            isContainAll = False
            for request in requests:
                if request.response:
                    if _urlStrs and len(_urlStrs) > 0:
                        for urlStr in _urlStrs:
                            if urlStr in request.url:
                                isContainAll = True
                            else:
                                isContainAll = False
                                break
                        if isContainAll and _configMethod in request.method:
                            if (_excludeStr != '' and _excludeStr not in request.url) | (_excludeStr == ''):
                                return request
            return None
        for api in apiKeys:
            # self.getRequsetInfo(api['curUrl'], api['actionText'], api['reqMethod'], api['excludeStr'], api['errCb'])
            curApiConfig = apiDict[api]
            _urlStrs = curApiConfig['urlStrs']
            _configMethod = curApiConfig['method']
            _remark = curApiConfig['remark']
            _excludeStr = curApiConfig['excludeStr']
            request = findApiRequest(_urlStrs, _configMethod, _excludeStr)

            if request and request.response:
                _status = request.response.status_code
                _params = request.body.decode('utf-8')
                _apiUrl = request.url
                _method = request.method
                _actionText = _remark
                _content = gzip.decompress(request.response.body)
                # # print('jsonContent----', _content.decode('utf-8'))
                print('jsonContent----', _apiUrl)
                # print('content----', gzip.decompress(_content))
                # 获取接口返回内容
                try:
                    _sucessContent = _content.decode('utf-8')
                    jsonContent = json.loads(_sucessContent)
                    # print('jsonContent----', jsonContent,
                    #       jsonContent['Success'])
                    if (jsonContent['Success'] != True):
                        self.logger.error(
                            _actionText + '失败: \n Request URL: {a} \n Request Method: {me} \n RequsetParams: {p} \n Status Code: {s} \n Code: {c} \n Message: {m}'.format(a=_apiUrl, me=_method, p=_params, s=_status, c=jsonContent['Code'], m=jsonContent['Message']))
                        errCb and errCb(self)
                    else:
                        self.logger.debug(
                            _actionText + '成功: \n Request URL: {a} \n Request Method: {me}'.format(a=_apiUrl, me=_method))
                    # return jsonContent
                    requests.pop(requests.index(request))
                    continue
                except:
                    print('error----')
                    requests.pop(requests.index(request))
                    continue
