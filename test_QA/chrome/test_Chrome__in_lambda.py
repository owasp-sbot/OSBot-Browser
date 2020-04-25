from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda


class test_Chrome_in_Lambda(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_browser.lambdas.dev.lambda_shell'
        self._lambda = Lambda(self.lambda_name)

    def test_update_lambda(self):
        self.result = Deploy().deploy_lambda__browser_dev(self.lambda_name)

    def test_update_and_invoke(self):
        #self.test_update_lambda()
        code = """
from osbot_aws.Dependencies import load_dependencies        
load_dependencies('pyppeteer,websocket-client')        
from osbot_browser.chrome.Chrome import Chrome       

#from osbot_utils.decorators.Sync import sync
#@sync
#async def browser(chrome):
#    return await chrome.browser_connect()
#browser =  browser(Chrome())

chrome = Chrome()
chrome.sync__setup_browser()
#result = browser.process.pid
     
browser = chrome.sync_browser()
result = browser.process.pid        
"""
        self.result = self._lambda.shell().python_exec(code)

    def test_invoke_shell_commands(self):
        shell = self.result = self._lambda.shell()
        self.result = shell.ls('/tmp')
        self.result = shell.list_processes()