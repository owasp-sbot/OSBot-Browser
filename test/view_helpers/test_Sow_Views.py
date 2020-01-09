from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Maps_Views import Maps_Views
from gw_bot.Deploy import Deploy
from osbot_browser.view_helpers.Sow_Views import Sow_Views


class Test_Sow_Views(TestCase):

    def setUp(self):
        Deploy().setup()                    # set local ossbot environment
        self.sow_views = Sow_Views()
        self.png_data   = None
        self.result     = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_default(self):
        self.png_data = self.sow_views.default(headless=False)#,channel='DJ8UA0RFT')

    def test_using_lambda(self):
        payload = {"params": ['render','/sow/simple.html',0,0,600,50]}
        self.lambda_name = 'osbot_browser.lambdas.lambda_browser'
        self.lambda_browser = Lambda(self.lambda_name)
        self.png_data  = self.lambda_browser.invoke(payload)