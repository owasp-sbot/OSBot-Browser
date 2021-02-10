import os

from pyppeteer.browser import Browser

from osbot_browser.chrome.Chrome_Args   import Chrome_Args
from osbot_utils.utils.Files            import temp_folder, file_exists
from osbot_utils.utils.Http             import port_is_open
from osbot_utils.utils.Json             import json_save, json_load_file
from osbot_utils.utils.Misc             import date_now
from osbot_utils.utils.Process          import chmod_x
from pyppeteer                          import connect, launch

CONNECT_METHOD_NO_BROWSER       = 'No browser open or connected'
CONNECT_METHOD_STARTED_CHROME   = 'Started chrome process'
CONNECT_METHOD_CONNECTED_CHROME = 'Connected to running chrome process'

class Chrome_Setup:

    def __init__(self, chrome_args, options):
        self._browser         : Browser     = None
        self.chrome_args      : Chrome_Args = chrome_args
        self.options          : dict        = options
        self.s3_chrome_binary : tuple       = ('gw-bot-lambdas','lambdas-dependencies/chromium-2_1_1')
        self.file_tmp_last_chrome_session   = '/tmp/browser-last_chrome_session.json'
        self.slow_motion      : int         = 0

    async def browser_setup(self):
        if self.running_on_aws():
            return await self.browser_setup_for_aws_execution()
        else:
            return await self.browser_setup_for_local_execution()

    async def browser_setup_for_aws_execution(self):
        self.aws_download_headless_chrome_from_s3()
        os.environ['PYPPETEER_HOME']    = '/tmp'    # tell pyppeteer to use this read-write path in Lambda aws
        self.chrome_args.args_set_user_data_dir(temp_folder())  # set userdata to folder inside /tmp (since that is writable)
        return await self.browser_launch_or_connect()

    async def browser_setup_for_local_execution(self):
        try:
            return await self.browser_launch_or_connect()
        except Exception as error:
            if "certificate verify failed'" in str(error):
                raise Exception("Chrome could not be downloaded due to SSL error. Root cause is lack of SSL certs in your system. \n"
                                "See https://github.com/pyppeteer/pyppeteer/issues/105 \n"
                                "See https://timonweb.com/python/fixing-certificate_verify_failed-error-when-trying-requests-html-out-on-mac/ \n") from None
            else:
                raise error

    async def browser_launch_or_connect(self):                                                          # currently used when connecting locally (not on AWS)
        if self.options.get('new_process'):                                                             # if configured to start a new process all the time
            return await self.browser_launch()                                                          # launch it
        else:
            if await self.browser_connect() is False:                                                         # if we were not able to connect to a previously running instance of Chrome
                self._browser = await self.browser_launch()                                             # start a new Chromium process
            return self._browser

    async def browser_connect(self):
        last_chrome_session = self.get_last_chrome_session()
        url_chrome = last_chrome_session.get('url_chrome')
        port       = last_chrome_session.get('port')
        if url_chrome and port_is_open(port):                                                       # needs pip install websocket-client
            kwargs = {
                        'browserWSEndpoint': url_chrome,
                        'slowMo'           : self.options['slowMo']  # todo: confirm this has no side effects when set to 0 (i.e. slow it down)
                    }
            self._browser = await connect(**kwargs)
            return True
        return False

    async def browser_launch(self):

        kwargs = {
                    "headless" : self.options['headless'  ],    # show UI
                    "autoClose": self.options['auto_close'],    # with False Chromium will not close when Unit Tests end
                    'slowMo'   : self.options['slowMo'    ],
                    "args"     : self.chrome_args.args()

                 }
        path_headless_shell = self.options.get('path_headless_shell')
        if path_headless_shell:                                 # if path if provided
            chmod_x(path_headless_shell)                        # make sure it is marked as executable
            kwargs['executablePath'] = path_headless_shell      # add it to the launch params
        self._browser  = await launch(**kwargs)

        self.set_last_chrome_session()
        return self._browser


    # Sync methods

    #  binary downloaded from https://github.com/alixaxel/chrome-aws-lambda/releases (which was the most recent compilation of chrome for AWS that I could find
    #  file created using: brotli -d chromium.br
    #  refefences: https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb#a2fb
    #todo: put this on an AWS speficic class (since it requires OSBot_AWS)
    def aws_download_headless_chrome_from_s3(self):
        from osbot_aws.apis.S3 import s3_file_download
        (s3_bucket, s3_key) = self.s3_chrome_binary
        headless_shell = s3_file_download(s3_bucket, s3_key, use_cache=True)
        self.options['path_headless_shell'] = headless_shell

    def connect_method(self):
        if self._browser is None:
            return CONNECT_METHOD_NO_BROWSER
        if self.process_id():
            return CONNECT_METHOD_STARTED_CHROME
        return CONNECT_METHOD_CONNECTED_CHROME

    def chrome_executable(self):
        if self.connect_method() == CONNECT_METHOD_NO_BROWSER:
            return None
        if self.connect_method() == CONNECT_METHOD_STARTED_CHROME:
            return self._browser.process.args[0]
        if self.connect_method() == CONNECT_METHOD_CONNECTED_CHROME:
            return self.get_last_chrome_session().get('process_args',[''])[0]

    def get_last_chrome_session(self):
        if file_exists(self.file_tmp_last_chrome_session):
            return json_load_file(self.file_tmp_last_chrome_session)
        return {}

    def process_id(self):
        if self._browser.process:
            return self._browser.process.pid

    def process_args(self):
        if self._browser.process:
            return self._browser.process.args
        return []

    def set_last_chrome_session(self):
        data = {
                 'process_args': self.process_args()     ,
                 'process_id'  : self.process_id()       ,
                 'url_chrome'  : self._browser.wsEndpoint,
                 'port'        : self._browser._connection.connection.remote_address[1],
                 'when'        : date_now()
                }
        json_save(data, self.file_tmp_last_chrome_session)
        return self

    def user_data_dir(self):
        for arg in self.process_args():
            if arg.startswith('--user-data-dir='):
                return arg.split('--user-data-dir=').pop()

    def running_on_aws(self):
        return os.getenv('AWS_REGION') is not None   # use this the AWS_REGION to determine if we are currently on AWS
