import base64
from time import sleep
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.sites.Web_Jira import Web_Jira


class test_Web_Jira(Test_Helper):
    def setUp(self):
        super().setUp()
        self.headless   = False
        self.result     = None
        self.png_data   = None
        self.new_page   = False
        self.web_jira   = Web_Jira(headless=self.headless,new_page=self.new_page).setup()
        self.close_wait = 0

    def tearDown(self):
        super().tearDown()

        if self.new_page:
            sleep(self.close_wait)
            self.web_jira.page.close()

    def test_issue(self):
        self.web_jira.issue('VP-1')

        self.web_jira.logout()
        self.web_jira.login()
        self.web_jira.fix_set_list_view()
        self.png_data = self.web_jira.issue('PERSON-1').fix_issue_remove_ui_elements().screenshot()


    def test_fix_issue_remove_ui_elements(self):
        self.web_jira.issue('VP-1')
        self.result = self.web_jira.fix_issue_remove_ui_elements()

    def test_login(self):
        self.result = self.web_jira.logout().login()
        #self.result =  self.web_jira.login()
        self.png_data = self.web_jira.screenshot()

    def test_logout(self):
        self.result = self.web_jira.logout()
        self.png_data = self.web_jira.screenshot()

    def test_open(self):
        path ='/'
        self.result = self.web_jira.open(path)
        #self.png_data = self.web_jira.screenshot()

    def test_screenshot(self):
        self.png_data = self.web_jira.screenshot()


