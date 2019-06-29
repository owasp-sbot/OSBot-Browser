import base64
import unittest

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Dev          import Dev

from oss_bot.Deploy import Deploy


class test_jira_web(unittest.TestCase):
    def setUp(self):
        self.png_data = None
        self.result = None
        self._lambda = Lambda('osbot_browser.lambdas.slack_web')


    def tearDown(self):
        if self.png_data:
            if type(self.png_data) is str:
                png_file = '/tmp/tmp-jira-screenshot.png'
                with open(png_file, "wb") as fh:
                    fh.write(base64.decodebytes(self.png_data.encode()))
                Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data),png_file))
            else:
                Dev.print(self.result)
        if self.result:
            Dev.print(self.result)

    #def test_invoke_directly(self):
    #    result = run({},{})
    #    assert result == '*Here are the `Browser_Commands` commands available:*'


    def test_invoke(self):
        self.test_update_lambda()
        target = '/messages/random/'

        payload = { 'target': target   ,
                    'channel': 'DDKUZTK6X' ,            # gsbot
                    'team_id': 'T7F3AUXGV' ,            # GS-CST
                    'width'  : 800,
                    'height' : 1000 }
        self.result = self._lambda.invoke(payload)
        #self.png_data = self.result# self._lambda.invoke(payload)
        self.png_data = self.result

    def test_invoke_oss(self):
        self.test_update_lambda()
        #target = '/messages/oss-helpdesk'
        target = '/messages/oss-general'

        payload = {'target'   : target      ,
                   'channel'  : 'DJ8UA0RFT' ,   # OSS - gsbot
                   'team_id'  : 'TAULHPATC' ,   # OSS
                   'width'    : 800         ,
                   'height'   : 600         ,
                   'delay'    : 0           ,
                   'scroll_by': '0'         }
        #self.result = self._lambda.invoke(payload)
        self.png_data = self._lambda.invoke(payload)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__slack_web()

    # def test_set_secret(self):
    #     self.result = Secrets('gs_bot_slack_web_oss').value(
