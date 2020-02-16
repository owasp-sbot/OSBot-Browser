from gw_bot.Deploy import Deploy
from osbot_aws.apis.Lambda import Lambda

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.lambdas.google_chart import run


class test_google_charts(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless    = True
        self.png_data    = None
        self.lambda_name = 'osbot_browser.lambdas.google_chart'
        self._lambda     = Lambda(self.lambda_name)
        self.chart_type  = 'LineChart'
        self.options     = {'title'    : 'An Chart (in Lambda)',
                            'curveType': 'function',
                            'legend'   : {'position': 'bottom'},
                            }
        self.data        = [['Year', 'Line 1', 'Line 2','Line 3'],
                            ['2004', 100, 400,30],
                            ['2005', 1170, 460,400],
                            ['2006', 660, 1120,100],
                            ['2007', 1030, 540,200],
                            ['2008', 1030, 540,250],
                            ['2009', 1030, 540,100]]
        self.params       = { 'chart_type':self.chart_type, 'options': self.options , 'data': self.data }

    # def tearDown(self):
    #     super().tearDown()
    #     if self.png_data:
    #         Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_invoke_directly(self):
        #params = { 'chart_type':self.chart_type, 'options': self.options , 'data': self.data}
        self.png_data = run(self.params,None)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser(self.lambda_name)

    def test_update_and_invoke(self):
        #self.test_update_lambda()
        self.png_data = self._lambda.invoke(self.params)
