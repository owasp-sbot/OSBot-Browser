

from pbx_gs_python_utils.utils.Files import Files

from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Render_Page import Render_Page
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers
#from oss_bot.lambdas.png_to_slack import load_dependency

class Maps(Base_View_Helpers):
    def __init__(self,headless=True):
        self.web_page = 'wardley-maps/empty.html'

        super().__init__(web_page=self.web_page,headless=headless)

    

class Maps_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False,headless=True):
        #load_dependency('syncer');
        #channel =  'DJ8UA0RFT'
        maps = Maps(headless)
        maps.load_page(True)

        maps.exec_js("maps.add_component('aaa' , 1, 1)")
        from time import sleep
        sleep(1)
        return maps.send_screenshot_to_slack('not-used', channel)

        #from osbot_browser.view_helpers.Google_Charts_Js import Google_Charts_Js
        #google_charts = Google_Charts_Js(headless).load_page()
        #return google_charts.send_screenshot_to_slack('not-used', channel)

    @staticmethod
    def exec_js(team_id=None, channel=None, params=None, no_render=False, headless=True):
        #channel = 'DJ8UA0RFT'
        js_code = " ".join(params)
        #load_dependency('syncer');
        js_code = js_code.replace('‘','"').replace('’','')

        maps = Maps(headless)
        maps.load_page(True)

        from time import sleep
        sleep(1)

        maps.exec_js(js_code)#"maps.add_component('aaa' , 1, 1)")
        return maps.send_screenshot_to_slack('not-used', channel)