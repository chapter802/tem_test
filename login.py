from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class TestLogin(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def test(self):
        self.driver.get('http://172.16.6.62:8080/login')
        sleep(1)
        self.driver.find_element(By.ID, 'userID').send_keys('selenium_test')
        sleep(1)
        self.driver.find_element(By.ID, 'password').send_keys('123456')
        sleep(1)
        self.driver.find_element(By.ID, 'login').click()
        sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    # test()
    case = TestLogin()
    case.test()
