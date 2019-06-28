import base64
import json
import unittest

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package

from osbot_browser.Deploy import Deploy
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_browser.browser.Browser_Commands import Browser_Commands
from osbot_browser.lambdas.lambda_browser   import run
from pbx_gs_python_utils.utils.Dev          import Dev


class test_jira_web(unittest.TestCase):
    def setUp(self):
        self.png_data = None
        self.result = None
        self._lambda = Lambda_Package('osbot_browser.lambdas.slack_web')


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
        self._lambda.update_code()
        target = '/messages/random/'

        payload = { 'target': target   ,
                    'channel': 'DDKUZTK6X' ,            # gsbot
                    'team_id': 'T7F3AUXGV' ,            # GS-CST
                    'width'  : 800,
                    'height' : 1000 }
        self.result = self._lambda.invoke(payload)
        self.png_data = self.result# self._lambda.invoke(payload)

    def test_invoke_oss(self):
        self._lambda.update_code()
        target = '/messages/oss-helpdesk'
        target = '/messages/oss-general'

        payload = {'target': target,
                   'channel': 'DDKUZTK6X',  # gsbot
                   #'team_id': 'T7F3AUXGV',  # GS-CST
                   'team_id': 'TAULHPATC',  # OSS
                   'width': 800,
                   'height': 4000}
        #self.result = self._lambda.invoke(payload)
        self.png_data = self._lambda.invoke(payload)

    def test_update_lambda(self):
        self._lambda.update_code()

