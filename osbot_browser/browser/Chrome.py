import os
from osbot_utils.utils.Files    import file_not_exists, file_copy, file_exists
from osbot_utils.utils.Http     import WS_is_open
from osbot_utils.utils.Json import json_save, json_load
from osbot_utils.utils.Process  import run_process
from pyppeteer                  import connect, launch


class Chrome():
    def __init__(self):
        self.options= self.default_options()
        self.file_tmp_last_chrome_session = '/tmp/browser-last_chrome_session.json'
        self.headless = True
        self._browser = None

    async def browser(self):
        if self._browser is None:
            self._browser = await self.browser_connect()
        return self._browser

    def default_options(self):
        options =  {
                        "headless"   : True ,
                        "new_browser": False        # think of better name
                   }
        return options



    # connect or open browser functions
    async def browser_connect(self):                                                        # currently used when connecting locally (not on AWS)

        url_chrome = None
        if not self.url_chrome:
            url_chrome = self.get_last_chrome_session()
        if url_chrome and WS_is_open(url_chrome):                                           # needs pip install websocket-client
            self._browser = await connect({'browserWSEndpoint': url_chrome})
        else:
            self._browser = await launch(headless=self.headless,
                                         #autoClose= self.auto_close,
                                         args=['--no-sandbox',
                                               #'--single-process',   # this option crashed chrome when logging in to Jira
                                               '--disable-dev-shm-usage'])
            self.set_last_chrome_session(self._browser.wsEndpoint)
        return self._browser

    #  binary downloaded from https://github.com/alixaxel/chrome-aws-lambda/releases (which was the most recent compilation of chrome for AWS that I could find
    #  file created using: brotli -d chromium.br
    #  refefences: https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb#a2fb
    def load_latest_version_of_chrome(self):
        source_file = '/tmp/lambdas-dependencies_chromium-2_1_1'            # todo: compile this ourselves
        target_file = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  #
        if file_not_exists(source_file):
            s3_bucket = 'gw-bot-lambdas'
            s3_key = 'lambdas-dependencies/chromium-2_1_1'
            from osbot_aws.apis.S3 import S3
            S3().file_download(s3_bucket, s3_key)
            file_copy(source_file, target_file)

    #todo: transform into async method
    def sync__setup_browser(self):                                                          # weirdly this works but the version below (using @sync) doesn't (we get an 'Read-only file system' error)
        import asyncio
        if os.getenv('AWS_REGION') is None:                                                 # we not in AWS so run the normal browser connect using pyppeteer normal method
            asyncio.get_event_loop().run_until_complete(self.browser_connect())
            return self

        self.load_latest_version_of_chrome()
        path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'     # path to headless_shell AWS Linux executable
        os.environ['PYPPETEER_HOME'] = '/tmp'                                                   # tell pyppeteer to use this read-write path in Lambda aws

        async def set_up_browser():  # todo: refactor this code into separate methods
            if self.new_browser:
                run_process("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
                self._browser = await launch(executablePath=path_headless_shell,                    # lauch chrome (i.e. headless_shell)
                                             args=['--no-sandbox'              ,
                                                   '--single-process'          ,
                                                   '--disable-dev-shm-usage'                        # one use case where this made the difference is when taking large Slack screenshots
                                                   ])                                               # two key settings or the requests will not work
            else:
                url_chrome = self.get_last_chrome_session()                                         # get url of last chrome session
                if url_chrome and WS_is_open(url_chrome):  # needs pip install websocket-client     # if it is still open
                    self._browser = await connect({'browserWSEndpoint': url_chrome})                # connect to it
                else:
                    run_process("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
                    self._browser = await launch(executablePath=path_headless_shell,                    # lauch chrome (i.e. headless_shell)
                                                 args=['--no-sandbox'              ,
                                                       '--single-process'          ,
                                                       '--disable-dev-shm-usage'                        # one use case where this made the difference is when taking large Slack screenshots
                                                       ])                                               # two key settings or the requests will not work
                self.set_last_chrome_session({'url_chrome': self._browser.wsEndpoint})              # save current endpoint (so that we can connect to it next time

        asyncio.get_event_loop().run_until_complete(set_up_browser())
        return self

    def get_last_chrome_session(self):
        if file_exists(self.file_tmp_last_chrome_session):
            return json_load(self.file_tmp_last_chrome_session).get('url_chrome')
        return {}

    def set_last_chrome_session(self, url_chrome):
        data = {'url_chrome': url_chrome}
        json_save(self.file_tmp_last_chrome_session, data)
        return self
