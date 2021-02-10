import base64
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_browser.browser.Browser_Page import Browser_Page


class test_Browser_Page(TestCase):
    def setUp(self):
        self.headless     = False
        self.new_page     = True
        self.page         = Browser_Page(headless=self.headless,new_page=self.new_page).setup()
        self.result       = None
        self.png_data     = None
        self.close_page   = True

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/tmp-jira-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

        if self.close_page:
            self.page.wait(2).close()

    def test_close(self):
        self.result = self.page.close()

    def test_open(self):
        self.result = self.page.open('https://www.google.com')

    def test_url(self):
        self.result = self.page.url()


