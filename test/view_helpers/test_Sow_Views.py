from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils.Dev import Dev

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from gw_bot.Deploy import Deploy
from osbot_browser.view_helpers.Sow_Views import Sow_Views


class Test_Sow_Views(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name    = 'osbot_browser.lambdas.lambda_browser'
        self.lambda_browser = Lambda(self.lambda_name)
        self.sow_views      = Sow_Views()
        self.png_data       = None
        self.result         = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_directly_default(self):
        self.png_data = self.sow_views.default(headless=False)

    def test_directly_view(self):
        self.png_data = self.sow_views.view(headless=False, params=['SOW-121'])

    def test_using_lambda_view(self):
        #self.test_update_lambda()
        payload = {"params": ['sow', 'view','SOW-119']}
        self.png_data = self.lambda_browser.invoke(payload)


    def test_using_lambda(self):
        payload = {"params": ['sow', 'default']}
        self.lambda_name = 'osbot_browser.lambdas.lambda_browser'
        self.lambda_browser = Lambda(self.lambda_name)
        self.result = self.lambda_browser.invoke(payload)
        #self.png_data  = self.lambda_browser.invoke(payload)



    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser()
        payload = {"params": ['sow', 'default']}
        self.result = self.lambda_browser.invoke(payload)








