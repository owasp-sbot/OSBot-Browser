from osbot_browser.py_query.Py_Query import Py_Query
from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.chrome import Chrome


class Temp_Browser:
    api_browser : API_Browser
    browser     : Chrome

    def __init__(self, headless=True):
        self.headless = headless

    def __enter__(self):
        self.api_browser = API_Browser(headless=self.headless)
        self.browser     = self.api_browser.sync__browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api_browser.sync__close_browser()

    def screenshot(self, save_to=None):
        return self.api_browser.sync__screenshot(file_screenshot=save_to)

    def html(self):
        return self.api_browser.sync__html_raw()

    def open(self, url):
        return self.api_browser.sync__open(url)

    def url(self):
        return self.api_browser.sync__url()

    def py_query(self):
        return Py_Query(self.html)