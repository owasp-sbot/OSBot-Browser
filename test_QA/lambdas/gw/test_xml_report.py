from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.lambdas.gw.xml_report import run
from gw_bot.Deploy import Deploy

class test_xml_report(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_browser.lambdas.gw.xml_report'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None
        self.png_data    = None

    def tearDown(self):
        super().print(self.result)
        super().save_png(self.png_data, '/tmp/lambda_png_file.png')

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser(self.lambda_name)

    def test_invoke_directly(self):
        payload = {"headless": False, "file_name": "the file", "json_data": self.json_report()}
        #self.result = run(payload, None).get('png_data')
        self.png_data = run(payload, None).get('png_data')

    def test__invoke_in_lambda(self):
        self.test_update_lambda()
        payload = { "file_name": "file.txt", "json_data": self.json_report()}
        self.png_data = self.aws_lambda.invoke(payload).get('png_data')


    def json_report(self):
        from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser
        test_file   = '/tmp/macros.xml-report.xml'
        xml_report  = Files.contents(test_file)
        parser      = Report_Xml_Parser(xml_report)
        json_report = parser.parse_document()
        return parser.analysis_report_summary(json_report)
