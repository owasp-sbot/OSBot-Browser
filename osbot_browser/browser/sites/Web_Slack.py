from time import sleep

from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Dev import Dev
from syncer import sync

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Browser_Page import Browser_Page


class Web_Slack:
    def __init__(self,headless=True, new_page=True):
        self._browser               = None
        self._browser_helper        = None
        self.server_details         = None
        self.server_url             = None
        self.secrets_id             = 'gs_bot_gs_Jira'
        self.headless               = headless
        self.new_page               = new_page
        self.page : Browser_Page    = None

    def setup(self):
        self.page           = Browser_Page(headless = self.headless, new_page=self.new_page).setup()
        self.server_details = Secrets(self.secrets_id).value_from_json_string()
        self.server_url     = self.server_details.get('server')
        return self

    def channel(self,issue_id):
        raise Exception('to do')
        #return self


    def login(self):
        path = '/login' # check
        self.open(path)
        page_text = self.page.text()

        if "Sign in to" in page_text:
            self.page.type('#email'   , self.server_details.get('username'))
            self.page.type('#password', self.server_details.get('password'))
            self.page.click('#signin_btn')
            self.page.wait_for_navigation()


    def logout(self):
        raise Exception('to do')
        # self.open('/logout')
        # if self.page.exists('#confirm-logout-submit'):
        #     self.page.click('#confirm-logout-submit')
        # return self

    def open(self, path):
        url = "{0}{1}".format(self.server_url, path)
        return self.page.open(url)

    def screenshot(self,width=None):
        if width:
            self.page.width(width)
        return self.page.screenshot()


    def fix_set_list_view(self):
        self.open('/issues/?filter=-1')
        self.page.javascript_eval("$('.aui-list-item-link').eq(1).click()")
        return self

    def fix_issue_remove_ui_elements(self):
        js_code =   """
                        //$('.input').hide()
                        $('.banner').hide()
                        $('.client_channels_list_container').hide()
                    """
        self.page.javascript_eval(js_code)
        return self