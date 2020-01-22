from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

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

    def json_report(self, test_file):
        from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser
        xml_report  = Files.contents(test_file)
        parser      = Report_Xml_Parser(xml_report)
        json_report = parser.parse_document()
        return parser.analysis_report_summary(json_report)

    def test_render_exec_summary(self):
        test_file  = '/tmp/macros.xml-report.xml'
        file_name  = 'Macros.xsl'
        json_report = self.json_report(test_file)
        self.result = self.xml_report.gw_exec_summary(file_name, json_report)

