from osbot_aws.apis.Lambda import Lambda

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
from osbot_utils.utils.Dev import pprint

from osbot_browser.Deploy import Deploy
from osbot_browser.lambdas.dev.browser_test import run


class test_browser_test(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless    = True
        self.lambda_name = 'osbot_browser.lambdas.dev.browser_test'
        self.handler     = run
        self.aws_lambda     = Lambda(self.lambda_name)

    def test_invoke_directly(self):
        # confirm 'lambda_sheel is working ok
        assert run({'lambda_shell': {'method_name':'ping', 'auth_key': Lambda_Shell().get_lambda_shell_auth()}}) == 'pong'

    def test_lambda_invoke(self):
        params = {'lambda_shell': {'method_name': 'ping', 'auth_key': Lambda_Shell().get_lambda_shell_auth()}}
        self.result = self.aws_lambda.invoke(params)

    def test_update_lambda(self):
        # note this lambda needs python 3.7 , with 3.8 it fails with error: "while loading shared libraries: libnss3.so"
        self.result = Deploy(self.handler).deploy_lambda__browser_dev()

    def test_update_and_invoke(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke({'url': 'https://www.google.com/'})
        #self.png_data = self._lambda.invoke({})













    def test_just_invoke(self):
        #payload = {'url': 'http://localhost:42195'}
        #payload = {'url': 'https://news.bbc.co.uk'}
        #payload = {}
        payload = {'url': 'https://www.google.com'}
        self.png_data = self.aws_lambda.invoke(payload)

    def test_invoke_shell_get_event_logs(self):
        print()
        print(self.aws_lambda.shell().ls('/tmp/event_log'))
        print(self.aws_lambda.shell().file_contents('/tmp/event_log/2020-04-12__00-20-34__258152.json'))

    def test_invoke_shell_list_processes(self):
        print(self.aws_lambda.shell().list_processes())
        print(self.aws_lambda.shell().disk_space())
        print(self.aws_lambda.shell().ls('/tmp -la'))



    #    for this to work run this command on the tests folder
    #         pip3 install -t _lambda_dependencies/websocket websocket
    #    GW-Bot/modules/OSBot-browser/_lambda_dependencies
    def test_upload_dependency(self):
        from osbot_aws.Dependencies import upload_dependency
        from osbot_aws.Dependencies import pip_install_dependency
        dependencies = ['websocket-client','syncer']
        for dependency in dependencies:
            pip_install_dependency(dependency)
            result = upload_dependency(dependency)
            pprint(result)


