import os
from typing import Optional

import pyppeteer
import pyppeteer.chromium_downloader
from pyppeteer.browser          import Browser
from pyppeteer                  import connect, launch
from osbot_utils.utils.Files    import file_not_exists, file_copy, file_exists
from osbot_utils.utils.Http     import WS_is_open
from osbot_utils.utils.Json     import json_save, json_load
from osbot_utils.utils.Process  import run_process



class Chrome():
    def __init__(self):
        self.options= self.default_options()
        self.file_tmp_last_chrome_session = '/tmp/browser-last_chrome_session.json'
        self._browser: Browser = None
        # add check for AWS execution
        self.osx_config()

    def osx_config(self):
        self.osx_set_chrome_version('722234')

    def default_options(self):
        options =  {
                        "headless"   : True,       # run with no UI
                        "auto_close" : True,       # auto close the chrome process after parent process stops (like in a unit test)
                        "new_process": True        # start a new chrome process every time
                   }
        return options

    async def browser(self):
        if self._browser is None:
            self._browser = await self.browser_connect()
            pass
        return self._browser



    async def browser_launch(self):
        args = ['--no-sandbox',
                #'--single-process',   # this option crashed chrome when logging in to Jira
                '--disable-dev-shm-usage'
                #'--enable-ui-devtools',
                #'--remote-debugging-port=9222'
                ]
        self._browser  = await launch(headless  = self.options['headless']  ,   # show UI
                                      autoClose = self.options['auto_close'],   # with False Chromium will not close when Unit Tests end
                                      args      = args)

        return self._browser

    async def browser_connect(self):                                                        # currently used when connecting locally (not on AWS)
        if self.options['new_process']:
            return await self.browser_launch()
        else:
            url_chrome = self.get_last_chrome_session()
            if url_chrome and WS_is_open(url_chrome):                                           # needs pip install websocket-client
                self._browser = await connect({'browserWSEndpoint': url_chrome})
            else:
                self._browser = await self.browser_launch()
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
            if self.options['new_browser']:
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

    # utils methods
    async def connection(self):
        return (await self.browser())._connection.connection

    async def port(self):
         return (await self.connection()).remote_address[1]

    async def ws_endpoint(self):
        return (await self.browser()).wsEndpoint
        #return browser._connection.connection.port
        #return self.sync_browser().

    async def version(self):
        return await (await self.browser()).version()

    # sync methods

    def headless(self, value=True):
        self.options['headless'   ] = value
        self.options['auto_close' ] = value
        self.options['new_process'] = value
        return self
    # see https://awesomeopensource.com/project/alixaxel/chrome-aws-lambda for a good list of value chrome_version values
    def osx_set_chrome_version(self, chrome_version):
        from pathlib import Path
        original_version = pyppeteer.__chromium_revision__
        os.environ['PYPPETEER_CHROMIUM_REVISION']               = chrome_version
        pyppeteer.__chromium_revision__                         = chrome_version
        pyppeteer.chromium_downloader.REVISION                  = chrome_version
        pyppeteer.chromium_downloader.chromiumExecutable["mac"] = Path(str(pyppeteer.chromium_downloader.chromiumExecutable["mac"]).replace(original_version, chrome_version))
        pyppeteer.chromium_downloader.downloadURLs["mac"]       = str(pyppeteer.chromium_downloader.downloadURLs["mac"]).replace(original_version, chrome_version)
        return self
    # # sync methods
    # @sync
    # async def sync_browser(self):
    #     return await self.browser()