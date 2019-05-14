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
        self._lambda = Lambda_Package('osbot_browser.lambdas.jira_web')


    def tearDown(self):
        if self.png_data:
            png_file = '/tmp/tmp-jira-screenshot.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data),png_file))
        if self.result:
            Dev.print(self.result)

    def test_invoke_directly(self):
        result = run({},{})
        assert result == '*Here are the `Browser_Commands` commands available:*'


    def test_invoke(self):
        self._lambda.update_code()
        payload ={ 'issue_id':  'GSP-95', 'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV'}
        self.result = self._lambda.invoke(payload)
        #self.png_data = self._lambda.invoke(payload)

    def test_update_lambda(self):
        self._lambda.update_code()

