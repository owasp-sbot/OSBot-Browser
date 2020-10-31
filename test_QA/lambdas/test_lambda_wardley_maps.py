import base64

from osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_utils.utils.Dev import Dev


class test_lambda_wardley_maps(Test_Helper):

    def setUp(self):
        self.lambda_name = 'osbot_browser.lambdas.lambda_browser'
        self.lambda_browser = Lambda(self.lambda_name) #lambdas.browser.lambda_browser')
        self.result   = None
        self.png_data = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser()

    def test_render__simple(self):
        payload = {"params": ['render','examples/wardley_map/simple.html']}
        self.png_data = self.lambda_browser.invoke(payload)

    def test_render__cup_of_tea(self):
        payload = {"params": ['render','examples/wardley_map/cup-of-tea.html']}
        #self.png_data = self.lambda_browser.invoke(payload)
        self.result = self.lambda_browser.invoke(payload)

    # def test_invoke_teamplate(self):
    #     super().setUp()
    #     aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
    #     payload = {"params": ["maps", "version"],
    #                'data': {}}
    #     self.result = aws_lambda.invoke(payload)

