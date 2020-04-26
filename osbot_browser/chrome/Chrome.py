import os
import pyppeteer
import pyppeteer.chromium_downloader
from pyppeteer.browser              import Browser

from osbot_browser.chrome.Chrome_Setup import Chrome_Setup
from osbot_utils.decorators.Sync    import sync

class Chrome():
    def __init__(self):
        self.options            : dict    = self.default_options()
        self._browser           : Browser = None
        self._chrome_args       : list    = self.get_default_chrome_args()
        self.chrome_setup                 = Chrome_Setup(chrome_args=self._chrome_args,options=self.options)

        self.osx_set_chrome_version('722234')  # 'HeadlessChrome/80.0.3987.0'

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

    def set_chrome_log_file(self, path):
        os.putenv('CHROME_LOG_FILE', path)
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