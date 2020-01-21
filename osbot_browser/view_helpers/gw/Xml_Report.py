from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Xml_Report(Base_View_Helpers):
    def __init__(self, headless=True, layout=None):
        if layout:
            self.web_page = '/sow/{0}.html'.format(layout)
        else:
            self.web_page = '/gw/xml-report-exec-summary.html'

        super().__init__(web_page=self.web_page, headless=headless)

    def gw_exec_summary(self, json_data):
        self.load_page(True)
