import os
import pyppeteer
import pyppeteer.chromium_downloader
from pyppeteer.browser              import Browser
from pyppeteer                      import connect, launch

from osbot_aws.apis.S3 import s3_file_download_to, s3_file_download
from osbot_utils.decorators.Sync    import sync
from osbot_utils.utils.Files import file_not_exists, file_exists, temp_folder, file_copy
from osbot_utils.utils.Http         import WS_is_open
from osbot_utils.utils.Json         import json_save, json_load
from osbot_utils.utils.Misc         import date_now
from osbot_utils.utils.Process import chmod_x, run_process

CONNECT_METHOD_NO_BROWSER       = 'No browser open or connected'
CONNECT_METHOD_STARTED_CHROME   = 'Started chrome process'
CONNECT_METHOD_CONNECTED_CHROME = 'Connected to running chrome process'

class Chrome():
    def __init__(self):
        self.options = self.default_options()
        self.file_tmp_last_chrome_session = '/tmp/browser-last_chrome_session.json'
        self._browser           : Browser = None
        self._chrome_args       : list    = self.get_default_chrome_args()
        self.osx_set_chrome_version('722234')       # 'HeadlessChrome/80.0.3987.0'

    def default_options(self):
        options =  {
                        "headless"           : True,    # run with no UI
                        "auto_close"         : True,    # auto close the chrome process after parent process stops (like in a unit test)
                        "new_process"        : True,    # start a new chrome process every time
                        "path_headless_shell": None     # use pyppeteer executable
                   }
        return options

    async def browser(self):
        if self._browser is None:
            self._browser = await self.browser_setup()
        return self._browser

    async def browser_setup(self):
        if self.running_on_aws():
            return await self.browser_setup_for_aws_execution()
        else:
            return await self.browser_setup_for_local_execution()

    async def browser_setup_for_aws_execution(self):
        self.aws_download_headless_chrome_from_s3()
        # = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  # path to headless_shell AWS Linux executable
        os.environ['PYPPETEER_HOME'] = '/tmp'  # tell pyppeteer to use this read-write path in Lambda aws

        user_data_dir = temp_folder()
        self.args_set_user_data_dir(user_data_dir)

        return await self.browser_launch_or_connect()

    async def browser_setup_for_local_execution(self):
        return await self.browser_launch_or_connect()

    async def browser_launch_or_connect(self):                                                          # currently used when connecting locally (not on AWS)
        if self.options.get('new_process'):                                                             # if configured to start a new process all the time
            return await self.browser_launch()                                                          # launch it
        else:
            if await self.browser_connect() is False:                                                         # if we were not able to connect to a previously running instance of Chrome
                self._browser = await self.browser_launch()                                             # start a new Chromium process
            return self._browser

    async def browser_connect(self):
        url_chrome = self.get_last_chrome_session().get('url_chrome')
        if url_chrome and WS_is_open(url_chrome):                                                       # needs pip install websocket-client
            self._browser = await connect({'browserWSEndpoint': url_chrome})
            return True
        return False

    async def browser_launch(self):

        #run_process("chmod", ['+x', path_headless_shell])  # set the privs of path_headless_shell to execute
        #self._browser = await launch(executablePath=path_headless_shell,  # lauch chrome (i.e. headless_shell)
        #                             args=self._chrome_args)

        kwargs = {
                    "headless" : self.options['headless'  ],    # show UI
                    "autoClose": self.options['auto_close'],    # with False Chromium will not close when Unit Tests end
                    "args"     : self._chrome_args
                 }
        path_headless_shell = self.options.get('path_headless_shell')
        if path_headless_shell:                                 # if path if provided
            chmod_x(path_headless_shell)                        # make sure it is marked as executable
            kwargs['executablePath'] = path_headless_shell      # add it to the launch params

        self._browser  = await launch(**kwargs)

        self.set_last_chrome_session()
        return self._browser

    async def close(self):
        browser = await self.browser()
        if browser:
            await browser.close()
        return self

    #  binary downloaded from https://github.com/alixaxel/chrome-aws-lambda/releases (which was the most recent compilation of chrome for AWS that I could find
    #  file created using: brotli -d chromium.br
    #  refefences: https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb#a2fb
    #todo: fix target_file location in chrome exec path
    def aws_download_headless_chrome_from_s3(self):
        source_file = '/tmp/lambdas-dependencies_chromium-2_1_1'            # todo: compile this ourselves
        target_file = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  #
        if file_not_exists(source_file):
            s3_bucket = 'gw-bot-lambdas'
            s3_key    = 'lambdas-dependencies/chromium-2_1_1'
            #s3_key    = 'lambdas-dependencies/chromium-2_0_2'
            s3_file_download(s3_bucket, s3_key)
            file_copy(source_file, target_file)

        self.options['path_headless_shell'] = target_file


    #todo: transform into async method
    def sync__setup_browser(self):                                                          # weirdly this works but the version below (using @sync) doesn't (we get an 'Read-only file system' error)
        import asyncio
        if os.getenv('AWS_REGION') is None:                                                 # we not in AWS so run the normal browser connect using pyppeteer normal method
            asyncio.get_event_loop().run_until_complete(self.browser_launch_or_connect())
            return self

        self.aws_download_headless_chrome_from_s3()
        path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'     # path to headless_shell AWS Linux executable
        os.environ['PYPPETEER_HOME'] = '/tmp'                                                   # tell pyppeteer to use this read-write path in Lambda aws

        user_data_dir = temp_folder()
        self.args_set_user_data_dir(user_data_dir)
        #return user_data_dir

        async def set_up_browser():  # todo: refactor this code into separate methods
            if self.options['new_process']:
                run_process("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
                self._browser = await launch(executablePath=path_headless_shell,                    # lauch chrome (i.e. headless_shell)
                                             args=self._chrome_args )
                                             # args=['--no-sandbox'              ,
                                             #       '--single-process'          ,
                                             #       '--disable-dev-shm-usage'                        # one use case where this made the difference is when taking large Slack screenshots
                                             #       ])                                               # two key settings or the requests will not work
            else:
                url_chrome = self.get_last_chrome_session().get('url_chrome')                                         # get url of last chrome session
                if url_chrome and WS_is_open(url_chrome):  # needs pip install websocket-client     # if it is still open
                    self._browser = await connect({'browserWSEndpoint': url_chrome})                # connect to it
                else:
                    run_process("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
                    self._browser = await launch(executablePath=path_headless_shell,                    # lauch chrome (i.e. headless_shell)
                                                 args=self._chrome_args
                                                       #'--no-sandbox'              ,
                                                       #'--single-process'          ,
                                                       #'--disable-dev-shm-usage'                        # one use case where this made the difference is when taking large Slack screenshots
                                                       )                                                 # two key settings or the requests will not work
                self.set_last_chrome_session()              # save current endpoint (so that we can connect to it next time

        asyncio.get_event_loop().run_until_complete(set_up_browser())
        return self

    def get_last_chrome_session(self):
        if file_exists(self.file_tmp_last_chrome_session):
            return json_load(self.file_tmp_last_chrome_session)
        return {}

    def set_last_chrome_session(self):
        data = {
                 'process_args': self.process_args()     ,
                 'process_id'  : self.process_id()       ,
                 'url_chrome'  : self._browser.wsEndpoint,
                 'when'        : date_now()
                }
        json_save(self.file_tmp_last_chrome_session, data)
        return self

    # utils methods
    async def connection(self):
        return (await self.browser())._connection.connection

    async def page(self):
        browser = await self.browser()
        return (await browser.pages()).pop()

    async def port(self):
         return (await self.connection()).remote_address[1]

    async def ws_endpoint(self):
        return (await self.browser()).wsEndpoint
        #return browser._connection.connection.port
        #return self.sync_browser().

    async def version(self):
        return await (await self.browser()).version()

    # sync methods

    def args_remove(self, item):
        if item in self._chrome_args:
            self._chrome_args.remove(item)
        return self

    def args_append(self,item):
        if item not in self._chrome_args:
            self._chrome_args.append(item)
        return self

    def args_remove_single_process(self      ): return self.args_remove('--single-process')
    def args_set_user_data_dir    (self, path): return self.args_append('--user-data-dir='+path)

    def chrome_executable(self):
        if self.connect_method() == CONNECT_METHOD_NO_BROWSER:
            return None
        if self.connect_method() == CONNECT_METHOD_STARTED_CHROME:
            return self._browser.process.args[0]
        if self.connect_method() == CONNECT_METHOD_CONNECTED_CHROME:
            return self.get_last_chrome_session().get('process_args',[''])[0]

    def enable_logging(self, log_file=None):
        self.args_append('--enable-logging')
        self.args_append('--v=1')
        if log_file:
            self.set_chrome_log_file(log_file)
        return self

    def get_default_chrome_args(self):
        return [                                # list from https://github.com/alixaxel/chrome-aws-lambda/blob/master/source/index.js#L72
                  '--no-sandbox'            ,   # most important ones
                  #'--disable-dev-shm-usage' ,   # most important ones
                  '--single-process'        ,   # most important ones (this has a nasty side effect when opening up Jira, the redirect crashes chrome)
                  #'--disable-background-timer-throttling',     # already added by puppeteer
                  #'--disable-breakpad',                        # already added by puppeteer
                  #'--disable-client-side-phishing-detection',  # already added by puppeteer
                  '--disable-cloud-import',
                  #'--disable-default-apps',                    # already added by puppeteer
                  #'--disable-extensions',                      # already added by puppeteer
                  '--disable-gesture-typing',
                  #'--disable-hang-monitor',                    # already added by puppeteer
                  '--disable-infobars',
                  '--disable-notifications',
                  '--disable-offer-store-unmasked-wallet-cards',
                  '--disable-offer-upload-credit-cards',
                  #'--disable-popup-blocking',                  # already added by puppeteer
                  '--disable-print-preview',
                  #'--disable-prompt-on-repost',                # already added by puppeteer
                  '--disable-setuid-sandbox',
                  '--disable-speech-api',
                  #'--disable-sync',                            # already added by puppeteer
                  '--disable-tab-for-desktop-share',
                  #'--disable-translate',                       # already added by puppeteer
                  '--disable-voice-input',
                  '--disable-wake-on-wifi',
                  '--disk-cache-size=33554432',
                  '--enable-async-dns',
                  '--enable-simple-cache-backend',
                  '--enable-tcp-fast-open',
                  '--enable-webgl',
                  '--hide-scrollbars',
                  '--ignore-gpu-blacklist',
                  '--media-cache-size=33554432',
                  #'--metrics-recording-only',                  # already added by puppeteer
                  '--mute-audio',
                  '--no-default-browser-check',
                  #'--no-first-run',                            # already added by puppeteer
                  '--no-pings',
                  '--no-zygote',
                  #'--password-store=basic',                    # already added by puppeteer
                  '--prerender-from-omnibox=disabled',
                  '--use-gl=swiftshader',
                  #'--use-mock-keychain',                       # already added by puppeteer
                ]

    def connect_method(self):
        if self._browser is None:
            return CONNECT_METHOD_NO_BROWSER
        if self.process_id():
            return CONNECT_METHOD_STARTED_CHROME
        return CONNECT_METHOD_CONNECTED_CHROME

    def keep_open(self):
        #self.options['headless'] = False
        self.options['auto_close' ] = False
        self.options['new_process'] = False
        return self

    def headless(self, value=True):
        self.options['headless'   ] = value
        self.options['auto_close' ] = value
        self.options['new_process'] = value
        return self

    def process_args(self):
        if self._browser.process:
            return self._browser.process.args
        return []

    def process_id(self):
        if self._browser.process:
            return self._browser.process.pid

    def running_on_aws(self):
        return os.getenv('AWS_REGION') is not None   # use this the AWS_REGION to determine if we are currently on AWS

    def set_chrome_log_file(self, path):
        os.putenv('CHROME_LOG_FILE', path)
        return self

    def user_data_dir(self):
        for arg in self.process_args():
            if arg.startswith('--user-data-dir='):
                return arg.split('--user-data-dir=').pop()

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

    # sync versions of async methods

    @sync
    async def sync_browser(self):
        return await self.browser()

    @sync
    async def sync_close(self):
        return await self.close()


    @sync
    async def sync_open(self, url):
        await (await self.page()).goto(url)
        return self

    @sync
    async def sync_url(self):
        return (await self.page()).url

    @sync
    async def sync_screenshot(self):
        return await (await self.page()).screenshot()