from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Sow(Base_View_Helpers):
    def __init__(self,headless=True, layout=None):
        if layout:
            self.web_page = '/sow/{0}.html'.format(layout)
        else:
            self.web_page = '/sow/simple.html'

        super().__init__(web_page=self.web_page,headless=headless)

class Sow_Views:
    current_version = "v0.20"

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False, headless=True):
        maps = Sow(headless)
        maps.load_page(True)
        return maps.send_screenshot_to_slack('not-used', channel)
