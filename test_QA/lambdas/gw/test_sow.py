from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.Deploy import Deploy
from osbot_browser.lambdas.gw.sow import run


class test_sow(Test_Helper):
    def setUp(self):
        self.lambda_name = 'osbot_browser.lambdas.gw.sow'
        self.oss_setup  = super().setUp()
        self.aws_lambda = super().lambda_package(self.lambda_name)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_invoke_directly(self):
        self.result = run({}, None)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser(self.lambda_name)


    def test__invoke(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke({})
