from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Maps_Views import Maps_Views
from oss_bot.Deploy import Deploy


class Test_Full_Calendar_Views(TestCase):

    def setUp(self):
        Deploy().setup()                    # set local ossbot environment
        self.maps_views = Maps_Views()
        self.png_data   = None
        self.result     = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_default(self):
        self.result = self.maps_views.default(headless=False)#,channel='DJ8UA0RFT')

    def test_exec_js(self):
        channel = 'DJ8UA0RFT'
        #channel = None
        params = ["maps.add_component('aaa 123' , 2, 1)"]

        self.result = self.maps_views.exec_js(headless=False ,channel=channel, params=params)

    def test_via_lambda_execution(self):
        self.test_update_lambda()
        view = 'default'
        code = ''
        aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        payload = {"params": ["maps", view, code],
                   'data': { 'channel' : 'DJ8UA0RFT'}}
        self.result = aws_lambda.invoke(payload)

    def test_via_lambda_execution__version(self):
        self.test_update_lambda()
        aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        payload = {"params": ["maps", "version"],'data': {}}
        self.result = aws_lambda.invoke(payload)

    def test_update_lambda_browser(self):
        Deploy().setup().deploy_lambda__browser()
        
    def test_update_lambda_oss_bot(self):
        Deploy().setup().deploy_lambda__oss_bot()