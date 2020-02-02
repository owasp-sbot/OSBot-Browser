import base64
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.Browser_Page import Browser_Page
from gw_bot.Deploy import Deploy


class test_Web_OSS(TestCase):
    def setUp(self):
        self.headless   = False
        self.result     = None
        self.png_data   = None
        self.new_page   = False
        self.close_wait = 0

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/tmp-web-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))


    def test_home_page(self):
        js_code ="""$('.inner_main_schedule').height(130);
                    $('.center_heading').height(-50)"""

        url = 'https://opensecsummit.org/schedule/day/mon/'
        from osbot_browser.browser.Browser_Page import Browser_Page
        page = Browser_Page(headless=True, new_page=True).setup()
        page.open(url)
        page.javascript_eval(js_code)


    def test_deploy_lambda__browser(self):
        Deploy().setup().deploy_lambda__browser()

