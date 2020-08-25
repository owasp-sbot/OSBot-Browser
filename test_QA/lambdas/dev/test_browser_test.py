from gw_bot.Deploy import Deploy
from osbot_aws.apis.Lambda import Lambda

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
from osbot_browser.lambdas.dev.browser_test import run


class test_browser_test(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless    = True
        self.lambda_name = 'osbot_browser.lambdas.dev.browser_test'
        self._lambda     = Lambda(self.lambda_name)

    def test_invoke_directly(self):
        # confirm 'lambda_sheel is working ok
        assert run({'lambda_shell': {'method_name':'ping', 'auth_key': Lambda_Shell().get_lambda_shell_auth()}}) == 'pong'

    def test_lambda_invoke(self):
        params = {'lambda_shell': {'method_name': 'ping', 'auth_key': Lambda_Shell().get_lambda_shell_auth()}}
        self.result = self._lambda.invoke(params)

    def test_update_lambda(self):
        # note this lambda needs python 3.7 , with 3.8 it fails with error: "while loading shared libraries: libnss3.so"
        self.result = Deploy().deploy_lambda__browser_dev(self.lambda_name)

    def test_update_and_invoke(self):
        self.test_update_lambda()
        self.result = self._lambda.invoke({'url': 'https://www.google.com/'})
        #self.png_data = self._lambda.invoke({})

    def test_just_invoke(self):
        payload = {'url': 'http://localhost:42195'}
        payload = {'url': 'https://www.google.com'}
        #payload = {'url': 'https://news.bbc.co.uk'}
        #payload = {}
        self.png_data = self._lambda.invoke(payload)
        #self.png_data = self._lambda.invoke(payload)

    def test_invoke_shell_get_event_logs(self):
        print()
        print(self._lambda.shell().ls('/tmp/event_log'))
        print(self._lambda.shell().file_contents('/tmp/event_log/2020-04-12__00-20-34__258152.json'))

    def test_invoke_shell_list_processes(self):
        print(self._lambda.shell().list_processes())
        print(self._lambda.shell().disk_space())
        print(self._lambda.shell().ls('/tmp -la'))



    #    for this to work run this command on the tests folder
    #         pip3 install -t _lambda_dependencies/websocket websocket
    #    GW-Bot/modules/OSBot-browser/_lambda_dependencies
    def test_upload_dependency(self):
        import websockets
        from osbot_aws.Dependencies import upload_dependency
        from osbot_aws.Dependencies import pip_install_dependency
        pip_install_dependency('websocket-client')
        self.result = upload_dependency('websocket-client')


