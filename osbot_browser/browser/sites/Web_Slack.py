from time import sleep

from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc
from syncer import sync

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Browser_Page import Browser_Page


class Web_Slack:
    def __init__(self, team_id, headless=True, new_page=True):
        self._browser               = None
        self._browser_helper        = None
        self.scroll_split           = 1500
        self.server_details         = None
        self.server_url             = None
        self.team_id                = team_id
        self.secrets_id             = self.resolve_secret_id()
        self.headless               = headless
        self.new_page               = new_page
        self.page : Browser_Page    = None


    def resolve_secret_id(self):
        if self.team_id == 'T7F3AUXGV' : return 'gs_bot_slack_web'
        if self.team_id == 'TAULHPATC' : return 'gs_bot_slack_web_oss'

    def setup(self):
        if self.secrets_id is None:
            raise Exception('in Web_Slack no slack team provided')
        self.page           = Browser_Page(headless = self.headless, new_page=self.new_page).setup()
        self.server_details = Secrets(self.secrets_id).value_from_json_string()
        self.server_url     = self.server_details.get('server')
        return self

    def channel(self,issue_id):
        raise Exception('to do')
        #return self

    def js_invoke(self,js_code):
        return self.page.javascript_eval(js_code)

    def login(self,wait_for_load=False):
        path = '/'
        self.open(path)

        page_text = self.page.text()

        if "Sign in to" in page_text:
            email = self.server_details.get('email')
            password = self.server_details.get('password')
            js_code = """
                          $('#email').val('{0}');
                          $('#password').val('{1}');
                          $('#signin_btn').click();
            """.format(email,password)
            self.page.javascript_eval(js_code)
            if wait_for_load:
                self.page.wait_for_element__id('msg_input')
                self.page.wait_for_element__id('loading_welcome_msg', exists=False)


            # misc tests to find optimal elements to wait
            #for i in range(0,3):
                #self.page.wait_for_element__id        ('msg_input'                                         )
                #self.page.wait_for_element__id        ('msg_input'          , max_attempts=4,exists=False )
                #self.page.wait_for_element__id        ('loading_welcome_msg', max_attempts=4, exists=True)
                #self.page.wait_for_element__id        ('loading_welcome_msg', max_attempts=4, exists=False)
                #self.page.wait_for_element__class_name('c-message__body'     , max_attempts=4, exists=True)
                #self.page.wait_for_element__class_name('c-message__body'     , max_attempts=4, exists=False)
                #self.page.wait_for_element__tag_name  ('button'              , max_attempts=4, exists=True)
                #self.page.wait_for_element__tag_name  ('button'              , max_attempts=4, exists=False)

                #print('****')



    def logout(self):
        logout_link_path_1 = "$('.ts_icon_sign_out').parent().parent().find('a').attr('href')"
        logout_link_path_2 = "$('#team_menu_user').click(); $('#logout a').attr('href')"
        logout_link      = self.page.javascript_eval(logout_link_path_1)
        if logout_link is None:
            logout_link = self.page.javascript_eval(logout_link_path_2)
        if logout_link and logout_link.startswith('https://slack.com/signout'):
            self.page.open(logout_link)
        else:
            print("didn't find logout link")
        return self

    def open(self, path=None):
        if path is None:
            path = ''
        url = "{0}{1}".format(self.server_url, path)

        page = self.page.open(url)
        self.page.wait_for_element__id('loading_welcome_msg', exists=False)
        return page

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

    def fix_set_list_view(self):
        self.open('/issues/?filter=-1')
        self.page.javascript_eval("$('.aui-list-item-link').eq(1).click()")
        return self

    def fix_ui_for_screenshot(self):
        js_code = """
                        $('.client_channels_list_container').hide();
        """
        self.page.javascript_eval(js_code)
        return self

    def scroll_messages_by(self,value):
        value = Misc.to_int(value)
        if value:
            # split the scroll in chunks since it was not working as expected when the
            # scroll amount was bigger than the current browser page window height
            while value > 0:
                if value < self.scroll_split:
                    scroll_by = value
                else:
                    scroll_by = self.scroll_split
                value -= scroll_by
                js_code = """value = $('.c-scrollbar__hider').eq(1).scrollTop() - {0} ;
                             $('.c-scrollbar__hider').eq(1).scrollTop(value);""".format(scroll_by)
                self.js_invoke(js_code)
                self.wait(0.25)             # wait a little bit before sending the next scroll event (this needs a better solution)

        return self
