from gw_bot.Deploy import Deploy
from osbot_aws.apis.Lambda import Lambda

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_browser.lambdas.aws_web import run


class test_google_charts(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless    = True
        self.lambda_name = 'osbot_browser.lambdas.aws_web'
        self._lambda     = Lambda(self.lambda_name)

    def tearDown(self):
        super().tearDown()

    def test_invoke_directly(self):
        self.png_data = run({},None)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser(self.lambda_name)

    def test_update_and_invoke(self):
        self.test_update_lambda()
        self.result = self._lambda.invoke({})
        #self.png_data = self._lambda.invoke({'channel': 'DRE51D4EM'})
