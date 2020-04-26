from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from osbot_utils.decorators.trace import trace



class test_Chrome_in_Lambda(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_browser.lambdas.dev.lambda_shell'
        self._lambda = Lambda(self.lambda_name)

    def test_update_lambda(self):
        self.result = Deploy().deploy_lambda__browser_dev(self.lambda_name)

    #@trace(include=['osbot*', 'boto*'])
    def test_reset_lambda(self):
        self.result = self._lambda.shell().reset()

    def test_update_and_invoke(self):
        code = """
from osbot_aws.Dependencies import load_dependencies
load_dependencies('pyppeteer2,websocket-client')
from osbot_browser.chrome.Chrome_Sync import Chrome_Sync

chrome = Chrome_Sync().keep_open()
chrome.browser()
#result = chrome.open('https://news.google.com').url()

from osbot_utils.utils.Misc import bytes_to_base64
result = bytes_to_base64(chrome.screenshot()) 

#result = chrome_sync.chrome.chrome_setup.connect_method()      
"""

        #self.test_update_lambda()
        #self.test_reset_lambda()

        self.png_data = self._lambda.shell().python_exec(code)

    def test_update_and_invoke__test(self):

        code = """
from osbot_aws.Dependencies import load_dependencies
        
load_dependencies('pyppeteer2,websocket-client')

from osbot_browser.chrome.Chrome import Chrome       

#chrome = Chrome().keep_open()
#from osbot_utils.utils.Http import GET
#result = GET('http://127.0.0.1:54433')
#result = chrome.get_last_chrome_session()     
#browser = chrome.sync_browser()                     # launch it 

#browser = Chrome().keep_open().sync_browser()       # attach 
#result = chrome.connect_method()

from osbot_utils.decorators.Sync    import sync
@sync
async def local_chrome():
    from osbot_browser.chrome.Chrome import Chrome
    from pyppeteer import connect, launch
    from osbot_utils.utils.Http import GET
    chrome = Chrome().keep_open()
    url_chrome =  chrome.get_last_chrome_session().get('url_chrome')
    
    #"ws://127.0.0.1:51059/devtools/browser/b2f81e97-78e6-417d-9487-4678b9b94121"
    # "ws://127.0.0.1:51059/devtools/browser/b2f81e97-78e6-417d-9487-4678b9b94121"
    #return url_chrome
    url = "http://127.0.0.1:51059/json/version"
        
    #return GET(url)
    await connect({'browserWSEndpoint': url_chrome})     
    return WS_is_open(url_chrome)
    await chrome.browser_connect()
    return chrome.connect_method() 

chrome = Chrome()#.keep_open()
chrome.sync_browser()
result = chrome.connect_method()

# Chrome().keep_open().sync__setup_browser()
# Chrome().keep_open().sync__setup_browser() #.sync_browser()
#result = local_chrome()

# @sync
# async def version():
#     from osbot_browser.chrome.Chrome import Chrome
#     return await Chrome().keep_open().version()
#     chrome = Chrome()
#     await chrome.browser()
#     return chrome.chrome_executable()
#     #'HeadlessChrome/67.0.3361.0'
#     
# result = version()
        
"""
        #self.test_update_lambda()
        self.result = self._lambda.shell().python_exec(code)

    #def test_get_browser_version(self):
    #'https://www.whatismybrowser.com/'

# test running webserver in Lambda
    def test_run_webserver_in_lambda(self):
        #self._lambda.shell().reset()
        #self.test_update_lambda()
        code = """
from osbot_aws.Dependencies import load_dependencies        
load_dependencies('pyppeteer,websocket-client')        
from osbot_browser.chrome.Chrome import Chrome       

chrome = Chrome()

load_dependencies('requests')   
from osbot_browser.browser.Web_Server import Web_Server
from osbot_utils.utils.Misc import bytes_to_base64
        
chrome.sync__setup_browser()
#page = chrome.sync_page()
#web_server = Web_Server()
#web_server.port = 1234
#web_server.start()
#with Web_Server() as web_server:    
#chrome.sync_open(web_server.url())
chrome.sync_open('http://localhost:1234/')
result = bytes_to_base64(chrome.sync_screenshot())
# 
# chrome.sync_open('https://www.google.com')
# bytes = chrome.sync_screenshot()
# import base64
# result =  base64.b64encode(bytes).decode()
# #result = chrome.sync_url()
"""

        self.png_data = self._lambda.shell().python_exec(code)

    def test_invoke_shell_commands(self):
        shell = self.result = self._lambda.shell()
        #self.result = shell.ls('/tmp')
        print('-----')
        print(shell.ps())
        #self.result = shell.memory_usage()
        print(shell.list_processes())



#todo: add chrome logs fetch
#todo: add ngrok support
#todo: news.google.com is not working
#bytes = chrome.sync_open('https://news.google.com')


