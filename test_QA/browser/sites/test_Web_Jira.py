import base64
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.sites.Web_Jira import Web_Jira


class test_Web_Jira(TestCase):
    def setUp(self):
        self.headless   = False
        self.result     = None
        self.png_data   = None
        self.new_page   = True
        self.web_jira   = Web_Jira(headless=self.headless,new_page=self.new_page).setup()
        self.close_wait = 0

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/tmp-jira-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

        if self.new_page:
            sleep(self.close_wait)
            self.web_jira.page.close()

    def test_issue(self):
        #self.web_jira.logout()
        #self.result = self.web_jira.login()
        #self.web_jira.fix_set_list_view()
        self.png_data = self.web_jira.issue('GSP-95').screenshot()


    def test_login(self):
        self.result = self.web_jira.logout().login()
        self.web_jira.fix_issue_remove_ui_elements()
        self.png_data = self.web_jira.screenshot()

    def test_open(self):
        path ='/'
        self.result = self.web_jira.open(path)
        self.png_data = self.web_jira.screenshot()



