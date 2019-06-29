import base64
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.sites.Web_Jira import Web_Jira
from osbot_browser.browser.sites.Web_Slack import Web_Slack


class test_Web_Slack(TestCase):
    def setUp(self):
        self.headless   = False
        self.result     = None
        self.png_data   = None
        self.new_page   = False
        #self.team_id    = 'T7F3AUXGV' #GS-CST
        self.team_id    = 'TAULHPATC'  #OSS
        self.web_slack  = Web_Slack(team_id=self.team_id, headless=self.headless, new_page=self.new_page).setup()
        self.close_wait = 0

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/tmp-jira-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

        #if self.new_page:
        #   sleep(self.close_wait)
        #   self.web_slack.page.close()

    # def test_channel(self):
    #     #self.web_jira.logout()
    #     self.web_skack.login()
    #     #self.web_jira.fix_set_list_view()
    #     self.png_data = self.web_jira.issue('GSP-95').fix_issue_remove_ui_elements().screenshot()

    def test_logout(self):
        self.result = self.web_slack.logout()

    def test_login(self):
        #self.web_slack.open('')
        #self.web_slack.page.wait_for_element__id('team_menu_user')
        #self.web_slack.page.wait_for_element__id('loading_welcome_msg', exists=False)
        #return
        self.result = self.web_slack.logout().login()
        print('after 2')
        self.png_data = self.web_slack.fix_ui_for_screenshot().screenshot()
        #self.web_slack.page.wait_for_navigation()

        #print(self.web_slack.wait(0.5).page.javascript_eval("$('#msg_input').length"))
        #print(self.web_slack.wait(0.5).page.javascript_eval("$('#msg_input').length"))
        #print(self.web_slack.wait(0.5).page.javascript_eval("$('#msg_input').length"))
        #print(self.web_slack.wait(0.5).page.javascript_eval("$('#msg_input').length"))
        #print(self.web_slack.page.javascript_eval("typeof($)"))

    def test_open(self):
        #path ='/messages/oss-helpdesk'
        path = '/messages/t-wardley-maps'
        path  = '/messages/oss-general'
        self.result = self.web_slack.open(path)
        #self.web_slack.set_browser_size(400,700)
        #self.web_slack.wait(1)
        self.web_slack.scroll_messages_by('-1600')

        self.png_data = self.web_slack.screenshot()













