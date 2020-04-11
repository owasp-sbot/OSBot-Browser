from gw_bot.Deploy import Deploy
from osbot_aws.apis.Lambda import Lambda

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.lambdas.aws_web import run


class test_google_charts(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless    = True
        self.lambda_name = 'osbot_browser.lambdas.dev.browser_test'
        self._lambda     = Lambda(self.lambda_name)


    def test_update_lambda(self):
        # note this lambda needs python 3.7 , with 3.8 it fails with error: "while loading shared libraries: libnss3.so"
        self.result = Deploy().setup().deploy_lambda__browser_dev(self.lambda_name)

    def test_update_and_invoke(self):
        self.test_update_lambda()
        self.png_data = self._lambda.invoke({'url': 'https://www.google.com/'})
        #self.png_data = self._lambda.invoke({})

    def test_just_invoke(self):
        payload = {'url': 'http://localhost:42195'}
        payload = {'url': 'https://www.google.com/asd'}
        payload = {'url': 'https://news.bbc.co.uk'}
        #payload = {}
        self.png_data = self._lambda.invoke(payload)

    def test_update_and_invoke_shell_command(self):
        #self.test_update_lambda()
        payload = {'shell_command': {'executable': 'bash', 'params': ['-c','ls /tmp'], 'cwd':'.'}}
        #payload = {'shell_command': {'executable': 'bash', 'params': ['-c', 'pwd'], 'cwd': '.'}}
        #payload = {'shell_command': {'executable': 'whoami', 'params': [], 'cwd': '.'}}
        payload = {'shell_command': {'executable': 'cat', 'params': ['/tmp/browser-last_chrome_session.json'], 'cwd': '.'}}
        #payload = {'shell_command': {'executable': 'ps', 'params': ['-aux'], 'cwd': '.'}}
        payload = {'shell_command': {'executable': 'ps', 'params': ['-o','pid,user,%mem,command','ax'], 'cwd': '.'}}
        self.result = self._lambda.invoke(payload)

    def test_invoke_eval(self):

        code = """
from osbot_browser.browser.API_Browser import API_Browser        
api_browser = API_Browser().sync__setup_browser()
#api_browser.sync__open('https://httpbin.org')
a = api_browser.auto_close
a=api_browser.sync__url()
#a = len(api_browser.sync__pages())

raise Exception(a)
        """
        payload = {'code': code}
        self.result = self._lambda.invoke(payload)

    #    for this to work run this command on the tests folder
    #         pip3 install -t _lambda_dependencies/websocket websocket
    #    GW-Bot/modules/OSBot-browser/_lambda_dependencies

    def test_upload_dependency(self):
        import websockets
        from osbot_aws.Dependencies import upload_dependency
        from osbot_aws.Dependencies import pip_install_dependency
        pip_install_dependency('websocket-client')
        self.result = upload_dependency('websocket-client')


