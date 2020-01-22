import base64
import json
import unittest

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Misc import Misc

from gw_bot.Deploy import Deploy
from osbot_browser.browser.Browser_Commands import Browser_Commands
from pbx_gs_python_utils.utils.Dev          import Dev

from osbot_browser.lambdas.jira_web import run


class test_jira_web(unittest.TestCase):
    def setUp(self):
        self.png_data = None
        self.result = None
        self._lambda = Lambda_Package('osbot_browser.lambdas.jira_web')


    def tearDown(self):
        if self.png_data:
            png_file = '/tmp/tmp-jira-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data),png_file))
        if self.result:
            Dev.print(self.result)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser('osbot_browser.lambdas.jira_web')

    def test_invoke_directly(self):
        issue_id = 'PERSON-1'
        payload = { 'issue_id' : issue_id }
        self.result = run(payload,{})
        #assert result == '*Here are the `Browser_Commands` commands available:*'


    def test_invoke(self):
        issue_id = 'PERSON-1'

        payload = { 'issue_id': issue_id   ,
                    'channel': 'DRE51D4EM' ,            # gwbot
                    'width'  : 2000,
                    'height' : 300 }
        self.result = self._lambda.invoke(payload)
        #self.png_data = self._lambda.invoke(payload)


