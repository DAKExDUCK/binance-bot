from seleniumwire import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from config import chrome_options


class Browser:
    def __init__(self) -> None:
        self.set_options()
        self.driver: WebDriver = webdriver.Chrome(executable_path='chromedriver.exe', options=self.chrome_options)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 5)

    def set_options(self):
        self.chrome_options = Options()
        for option in chrome_options:
            self.chrome_options.add_argument(option)

    def get_cookies_data(self):
        cookies = {}
        session_cookies = self.driver.get_cookies()
        for cookie in session_cookies:
            cookies[cookie['name']] = cookie['value']
        return cookies

    def get_headers(self):
        req_list = []
        for request in self.driver.requests:
            url_temp = request.url
            headers_temp = request.headers
            req_list.append([url_temp, headers_temp])

        req_list.reverse()

        for url_temp, headers_temp in req_list:
            if url_temp == 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search':
                return dict(headers_temp)