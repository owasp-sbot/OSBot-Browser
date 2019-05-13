from time import sleep

from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Dev import Dev
from syncer import sync

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Browser_Page import Browser_Page


class Web_Jira:
    def __init__(self,headless=True, new_page=True):
        self._browser               = None
        self._browser_helper        = None
        self.server_details         = None
        self.server_url             = None
        self.secrets_id             = 'GS_BOT_GS_JIRA'
        self.headless               = headless
        self.new_page               = new_page
        self.page : Browser_Page    = None

    def setup(self):
        self.page           = Browser_Page(headless = self.headless, new_page=self.new_page).setup()
        self.server_details = Secrets(self.secrets_id).value_from_json_string()
        self.server_url     = self.server_details.get('server')

        self.page.on_dialog__always_accept()
        return self

    # def browser(self):
    #     if self._browser is None:
    #         self._browser_helper = Browser_Lamdba_Helper(headless=self.headless).setup()
    #         self._browser        = self._browser_helper.api_browser
    #     return self._browser


    # async def login_async(self):
    #     (server, username, password) = self.server_details().values()
    #     await self.open(server + '/login.jsp')
    #     page = await self.browser().page()
    #     #await page.type('#login-form-username', username)
    #     #await page.type('#login-form-password', password)
    #     #await page.click('#login-form-submit')

    def issue(self,issue_id):
        #(server, username, password) = self.server_details().values()
        path =  '/browse/{0}'.format(issue_id)
        self.open(path)
        #self.browser().sync__await_for_element('.jira-help-tip')
        #self.browser().sync__js_execute("$('.jira-help-tip').hide()")

        return self

    def login(self):
        path = '/login.jsp?os_destination=/rest/helptips/1.0/tips'
        self.open(path)
        page_text = self.page.text()
        # (server, username, password) = self.server_details().values()
        # url = server + '/login.jsp?os_destination=/rest/helptips/1.0/tips'
        # page = self.browser().sync__page__with_auto_dialog_accept()
        # self.browser().sync__open(url)
        # page_text = self.browser().sync__page_text()
        #
        if "Username" in page_text:
            self.page.type('#login-form-username', self.server_details.get('username'))
            self.page.type('#login-form-password', self.server_details.get('password'))
            self.page.javascript_eval('document.forms[1].submit()')
            self.page.wait_for_navigation()
        #     self.browser().sync__type (page, '#login-form-password', password)
        #     #self.browser().sync__click(page, '#login-form-submit')
        #     self.browser().sync__js_execute('document.forms[1].submit()')
        #     self.browser().sync__wait_for_navigation()
        # #self.browser().sync__open(url)
        # #page_text = self.browser().sync__page_text()
        # html_start = '<html><head></head><body><pre style="word-wrap: break-word; '
        # return html_start in self.browser().sync__html_raw()
        #return page_text == '["newsletter-signup-tip"]'

    def logout(self):
        self.open('/logout')
        if self.page.exists('#confirm-logout-submit'):
            self.page.click('#confirm-logout-submit')
        return self

    def open(self, path):
        url = "{0}{1}".format(self.server_url, path)
        return self.page.open(url)

    def screenshot(self):
        return self.page.screenshot()