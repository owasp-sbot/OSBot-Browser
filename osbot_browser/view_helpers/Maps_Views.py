

from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Render_Page import Render_Page
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers
#from gw_bot.lambdas.png_to_slack import load_dependency

class Maps(Base_View_Helpers):
    def __init__(self,headless=True, page=None):
        if page:
            self.web_page = 'wardley-maps/{0}.html'.format(page)
        else:
            self.web_page = 'wardley-maps/empty.html'

        super().__init__(web_page=self.web_page,headless=headless)



class Maps_Views:

    current_version = "v0.20"

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False,headless=True):
        maps = Maps(headless)
        maps.load_page(True)
        return maps.send_screenshot_to_slack('not-used', channel)

    @staticmethod
    def render(team_id=None, channel=None, params=None, no_render=False, headless=True):
        page = Misc.array_pop(params,0)
        if page is None:
            return ':red_circle: you need to provide a map to render, try `cup-of-tea`'
        maps = Maps(headless,page)
        maps.load_page(True)
        return maps.send_screenshot_to_slack('not-used', channel)

    @staticmethod
    def exec_js(team_id=None, channel=None, params=None, no_render=False, headless=True):
        #channel = 'DJ8UA0RFT'
        user_code = " ".join(params)
        slack_message(':world_map: Creating wardley Map for code with size {0}'.format(len(user_code)), [], channel)
        user_code = user_code.replace('‘','"').replace('’','"').replace("```","")
        js_code = js_code = """   
                                  add            = window.maps.add_component;
                                  add_component  = window.maps.add_component;
                                  add_node       = window.maps.add_component;
                                  link           = function(to, from) { window.maps.add_connection(to, from) }
                                  add_connection = function(to, from) { window.maps.add_connection(to, from) }                                                                    
                                  add_edge       = function(to, from) { window.maps.add_connection(to, from) }
                                  
                        """ + user_code
        maps = Maps(headless)
        maps.load_page(True)

        maps.exec_js(js_code)
        return maps.send_screenshot_to_slack('not-used', channel)

    @staticmethod
    def version(*event):
        return Maps_Views.current_version
