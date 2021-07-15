import os
from sys import platform

import pyppeteer
import pyppeteer.chromium_downloader
from pyppeteer.browser              import Browser

from osbot_browser.chrome.Chrome_Args import Chrome_Args
from osbot_browser.chrome.Chrome_Setup import Chrome_Setup

class Chrome():
    def __init__(self, headless=True, osx_chrome_version='884014'):
        self.options        : dict         = self.default_options()
        self._browser       : Browser      = None
        self.chrome_args    : Chrome_Args  = Chrome_Args()
        self.chrome_setup   : Chrome_Setup = Chrome_Setup(chrome_args=self.chrome_args,options=self.options)

        # todo: move value below to a global config CONST value
        #self.osx_set_chrome_version('722234')  # 'HeadlessChrome/80.0.3987.0' (May 2020)
        #self.osx_set_chrome_version('800071')  # 'HeadlessChrome/86.0.4240.0' (Sep 2020)
        #self.osx_set_chrome_version('848005')  # 'HeadlessChrome/90.0.4403.0' (Feb 2021)
        #self.osx_set_chrome_version('884014')  # 'HeadlessChrome/90.0.4403.0' (Feb 2021)
        self.osx_set_chrome_version(osx_chrome_version)

        self.headless(headless)


    def default_options(self):
        options =  {
                        "headless"           : True,    # run with no UI
                        "auto_close"         : True,    # auto close the chrome process after parent process stops (like in a unit test)
                        "new_process"        : True,    # start a new chrome process every time
                        "path_headless_shell": None,    # use pyppeteer executable
                        "slowMo"             : 0
                   }
        return options

    async def browser(self):
        if self._browser is None:
            self._browser = await self.chrome_setup.browser_setup()
        return self._browser

    async def close(self):
        browser = await self.browser()
        if browser:
            await browser.close()
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

    def keep_open(self):
        self.options['auto_close' ] = False
        self.options['new_process'] = False
        return self

    def headless(self, value=True):
        self.options['headless'   ] = value
        self.options['auto_close' ] = value
        self.options['new_process'] = value
        return self

    def ignore_cert_errors(self):
        self.chrome_args.args_append('--ignore-certificate-errors')
        return self

    def slow_chrome_by(self, value):
        self.options['slowMo'] = value
        return self

    def sync(self):
        from osbot_browser.chrome.Chrome_Sync import Chrome_Sync
        return Chrome_Sync(self)

    # see https://awesomeopensource.com/project/alixaxel/chrome-aws-lambda for a good list of value chrome_version values
    def osx_set_chrome_version(self, chrome_version):
        if platform == "darwin" and chrome_version:
            from pathlib import Path
            original_version = pyppeteer.__chromium_revision__
            os.environ['PYPPETEER_CHROMIUM_REVISION']               = chrome_version
            pyppeteer.__chromium_revision__                         = chrome_version
            pyppeteer.chromium_downloader.REVISION                  = chrome_version
            pyppeteer.chromium_downloader.chromiumExecutable["mac"] = Path(str(pyppeteer.chromium_downloader.chromiumExecutable["mac"]).replace(original_version, chrome_version))
            pyppeteer.chromium_downloader.downloadURLs["mac"]       = str(pyppeteer.chromium_downloader.downloadURLs["mac"]).replace(original_version, chrome_version)
        return self