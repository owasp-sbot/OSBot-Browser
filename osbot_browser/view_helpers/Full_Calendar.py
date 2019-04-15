from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Full_Calendar(Base_View_Helpers):
    def __init__(self,headless=True, layout=None):
        if layout:
            self.web_page = '/full-calendar/{0}.html'.format(layout)
        else:
            self.web_page = '/full-calendar/simple.html'

        super().__init__(web_page=self.web_page,headless=headless)
