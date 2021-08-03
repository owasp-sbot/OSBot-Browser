from osbot_browser.py_query.Py_Query import Py_Query
from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.chrome import Chrome


class Temp_Browser:
    api_browser : API_Browser
    browser     : Chrome

    def __init__(self, headless=True, auto_close=True, open_page=None):
        self.headless   = headless
        self.auto_close = auto_close
        self.open_page  = open_page
        self.temp_screenshot_file = '/tmp/temp_browser_screenshot.png'

    def __enter__(self):
        self.api_browser = API_Browser(headless=self.headless)
        self.browser     = self.api_browser.sync__browser()
        if self.open_page:
            self.api_browser.sync__open(self.open_page)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_close is True:
            self.api_browser.sync__close_browser()              # todo see if this really only continues when the process process has terminated

    def links(self):
        return self.py_query().query('a').indexed_by_attribute('href', return_unique_list=True)
    def screenshot(self, save_to=None):
        if save_to is None:
            save_to = self.temp_screenshot_file
        return self.api_browser.sync__screenshot(file_screenshot=save_to)

    def html(self):
        return self.api_browser.sync__html_raw()

    def open(self, url):
        return self.api_browser.sync__open(url)

    def open_google(self):
        return self.open('https://www.google.com')

    def page(self):
        return self.api_browser.sync__page()

    def url(self):
        return self.api_browser.sync__url()

    def py_query(self):
        return Py_Query(self.html())

    def set_auto_close(self, value):
        self.auto_close = value