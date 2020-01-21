from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.gw.Xml_Report import Xml_Report


class Test_Xml_Report(TestCase):

    def setUp(self):
        #Deploy().setup()                    # set local ossbot environment
        self.headless       = False
        self.xml_report     = Xml_Report(headless=self.headless)
        self.png_data       = None
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_render_exec_summary(self):
        xml_report = 'asd'
        self.xml_report.gw_exec_summary(xml_report)
