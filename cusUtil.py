from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import platform
import pickle
import random
import string


def get_logger():
    import logging
    import logging.handlers
    import datetime
    import os

    cwd = os.getcwd()

    if not os.path.exists("Logs"):
        os.makedirs("Logs")

    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler(cwd + '/Logs/all.log', when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler(cwd + '/Logs/error.log')
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
