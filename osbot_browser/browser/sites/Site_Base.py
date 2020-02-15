from osbot_aws.apis.Secrets import Secrets

from osbot_browser.browser.Browser_Page import Browser_Page


class Site_Base:
    def __init__(self, headless=True):
        self._browser               = None
        self._browser_helper        = None
        self.server_details         = None
        self.login_details          = None
        self.server_url             = None
        self.secrets_id             = 'gw-bot-aws-console'
        self.headless               = headless
        self.new_page               = headless
        self.page : Browser_Page    = None



    def setup(self):
        self.page           = Browser_Page(headless = self.headless, new_page=self.new_page).setup()
        return self

    def js_invoke(self,js_code):
        return self.page.javascript_eval(js_code)

    def open(self, path=None):
        if path is None:
            path = ''
        url = "{0}{1}".format(self.server_url, path)

        return self.page.open(url)

    def wait(self,seconds):
        self.page.wait(seconds)
        return self

    def screenshot(self,width=None):
        if width:
            self.page.width(width)
        return self.page.screenshot()

    def set_browser_size(self,width, height):
        self.page.width(width, height)
        return self