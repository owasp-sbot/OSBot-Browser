from syncer import sync

from osbot_browser.browser.Web_Server import Web_Server
from osbot_browser.chrome.Chrome import Chrome
from osbot_browser.chrome.Chrome_Setup import Chrome_Setup
from osbot_browser.chrome.Chrome_Sync import Chrome_Sync
from osbot_utils.testing.Unit_Test import Unit_Test
from osbot_utils.utils.Files import temp_file, file_delete, file_contents, temp_folder, path_combine, file_exists
from osbot_utils.utils.Http import port_is_open, GET, port_is_not_open
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import bytes_to_base64


class test_Chrome(Unit_Test):       # todo: move some of the tests to the Chrome_Setup class

    def setUp(self):
        super().setUp()
        self.chrome = Chrome()

    @sync
    async def test_browser(self):
        browser = await self.chrome.browser()
        port    = await self.chrome.port()
        assert type(browser).__name__ == 'Browser'
        assert port_is_open(port)
        assert (await browser.pages()).pop().url == 'about:blank'

    async def test_browser_connect(self):
        browser = await self.chrome.browser_launch_or_connect()
        port    = await self.chrome.port()
        assert type(browser).__name__ == 'Browser'
        assert port_is_open(port)


    @sync
    async def test_chrome_executable(self):
        assert self.chrome.chrome_setup.chrome_executable() is None
        chrome_1 = Chrome().keep_open()
        await chrome_1.browser()
        assert 'Support/pyppeteer/local-chromium' in chrome_1.chrome_setup.chrome_executable()
        chrome_2 = Chrome().keep_open()
        await chrome_2.browser()
        assert 'Support/pyppeteer/local-chromium' in chrome_2.chrome_setup.chrome_executable()
        await chrome_2.close()


    @sync
    async def test_open(self):
        browser = await self.chrome.browser()
        url = 'https://www.google.com/404'
        #url = 'https://news.bbc.co.uk'
        #url = 'https://file-drop.co.uk/aaaa'
        # url = 'https://www.whatismybrowser.com/'
        page     = await browser.newPage()
        response = await page.goto(url)
        assert response.url == url
        assert response.status == 404

        # png_data = await page.screenshot()
        #self.png_data = (await page.screenshot())

    @sync
    async def test_get_last_chrome_session(self):
        self.chrome.keep_open()
        browser = await self.chrome.browser()
        assert set(json_load_file(self.chrome.chrome_setup.file_tmp_last_chrome_session)) == {'process_args', 'process_id', 'port', 'when','url_chrome'}
        await browser.close()

    @sync
    async def test_keep_open(self):
        file_delete(Chrome_Setup(None,None).file_tmp_last_chrome_session)
        url_1 = 'https://www.google.com/404'
        url_2 = 'https://www.google.com/ABC'
        chrome_1  = Chrome().keep_open()                            # 1st chrome object (with keep_open setting)
        browser_1 = await chrome_1.browser()                        # open process and get browser object
        page_1    = (await browser_1.pages()).pop()                 # get first page
        await page_1.goto(url_1)                                    # open 404 in google
        assert page_1.url == url_1                                  # confirm url

        chrome_2 = Chrome().keep_open()                             # create 2nd chrome object
        browser_2 = await chrome_2.browser()                        # connect to chrome and get browser object
        page_2    = (await browser_2.pages()).pop()                 # get page object
        assert page_2.url == url_1                                  # confirm url

        await page_2.goto(url_2)                                    # open another page in browser_2
        assert page_1.url == url_2                                  # confirm it was opened in browser 1
        assert page_2.url == url_2                                  # and in browser_2

        chrome_3 = Chrome().keep_open()                             # create 3rd chrome object
        browser_3 = await chrome_3.browser()                        # connect to chrome and get browser object
        page_3    = (await browser_3.pages()).pop()                 # get page object
        assert page_3.url == url_2                                  # confirm url

        assert self.chrome.chrome_setup.connect_method() == 'No browser open or connected'
        assert chrome_1.chrome_setup.connect_method()    == 'Started chrome process'
        assert chrome_2.chrome_setup.connect_method()    == 'Connected to running chrome process'
        assert chrome_3.chrome_setup.connect_method()    == 'Connected to running chrome process'
        #await browser_1.close()
        await browser_3.close()                                    # close browser

    @sync
    async def test_connection(self):
        connection = await self.chrome.connection()
        assert connection.closed              == False
        assert connection.open                == True
        assert connection.remote_address[0]   == '127.0.0.1'
        assert port_is_open(connection.remote_address[1])

    @sync
    async def test_port(self):
        assert port_is_open(await self.chrome.port())
        browser = await self.chrome.browser()
        assert (await browser.pages()).pop().url == 'about:blank'

    @sync
    async def test_process_args(self):
        await self.chrome.browser()
        assert '--no-sandbox' in self.chrome.chrome_setup.process_args()

    @sync
    async def test_user_data_dir(self):
        user_data_dir = temp_folder()
        self.chrome.chrome_args.args_set_user_data_dir(user_data_dir)
        await self.chrome.browser()
        assert self.chrome.chrome_setup.user_data_dir() == user_data_dir

    @sync
    async def test_version(self):
        assert await self.chrome.version() == 'HeadlessChrome/80.0.3987.0'

    @sync
    async def test_port(self):
        ws_endpoint = await self.chrome.ws_endpoint()
        port        = await self.chrome.port()
        assert ws_endpoint.startswith(f'ws://127.0.0.1:{port}')

        assert port_is_open    (port  )
        assert port_is_not_open(port+1)

    @sync
    async def test_osx_set_chrome_version(self):

        # the first time this test executes, it will download these versions of Chromium
        # path will be something like: /Users/diniscruz/Library/Application\ Support/pyppeteer/local-chromium/722234
        # see ids from https://github.com/alixaxel/chrome-aws-lambda ('Versioning' section)
        assert await Chrome()                                 .version() == 'HeadlessChrome/86.0.4240.0' # set to 800071
        assert await Chrome().osx_set_chrome_version('588429').version() == 'HeadlessChrome/71.0.3542.0' # current pyppeteer default (see value hardcoded at pyppeteer.__chromium_revision__ )
        #assert await Chrome().osx_set_chrome_version('575458').version() == 'HeadlessChrome/69.0.3494.0'
        #assert await Chrome().osx_set_chrome_version('664010').version() == 'HeadlessChrome/76.0.3807.0'
        assert await Chrome().osx_set_chrome_version('722234').version() == 'HeadlessChrome/80.0.3987.0' # previous
        assert await Chrome().osx_set_chrome_version('800071').version() == 'HeadlessChrome/86.0.4240.0' # current
        #assert await Chrome().osx_set_chrome_version('737173').version() == 'HeadlessChrome/81.0.4044.0'  # latest stable (as of 13/April) - see https://chromium.woolyss.com/ for list


    # Use case tests

    @sync
    async def test_confirm_chrome_starts_in_new_process(self):
        pid_1 = (await Chrome().browser()).process.pid
        pid_2 = (await Chrome().browser()).process.pid
        assert pid_1 > 10
        assert pid_1 != pid_2

    # this one will cause https://github.com/puppeteer/puppeteer/issues/4752
    # to solve use a variation of: sudo codesign --force --deep --sign - "/Users/diniscruz/Library/Application Support/pyppeteer/local-chromium/722234/chrome-mac/Chromium.app"
    # todo: improve this workflow since it is still not stable
    # @sync
    # async def test_headless(self):
    #     chrome = Chrome().headless(False)
    #     browser = await chrome.browser()
    #     url = 'https://www.whatismybrowser.com/'
    #     page    = await browser.newPage()
    #     await page.goto(url)
    #     assert page.url == url
    #     await page.close()
    #     await browser.close()

    @sync
    async def test_args_set_user_data_dir__enable_logging(self):
        user_data = temp_folder()
        chrome = Chrome().headless(True)
        (chrome.chrome_args.args_set_user_data_dir(user_data)
                           .enable_logging())
        await chrome.browser()
        log_file = path_combine(user_data, 'Default/chrome_debug.log')
        assert file_exists(log_file)

    @sync
    async def test_set_chrome_log_file(self):
        log_file = '/tmp/chrome_logfile.log'
        file_delete(log_file)
        chrome = Chrome().headless(True)
        chrome.chrome_args.enable_logging(log_file)
        await chrome.browser()
        assert 'Could not get the download directory.' in file_contents(log_file).split('\n').pop(0)

    @sync
    async def test_screenshot_jira(self):
        chrome  = Chrome()
        browser = await chrome.browser()
        page    = (await browser.pages()).pop()
        with Web_Server() as web_server:
            await page.goto(web_server.url())
            self.png_data = await page.screenshot()


    # test sites

    def test_run_chrome_locally(self):
        path_headless_shell = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chrome = Chrome().keep_open()
        chrome.options['path_headless_shell'] = path_headless_shell
        chrome_sync = Chrome_Sync(chrome)
        chrome_sync.browser()
        chrome_sync.open('https://www.google.com')
        self.png_data = bytes_to_base64(chrome_sync.screenshot())
        chrome_sync.close()

    @sync
    async def test_site__headless_news_google_com(self):
        chrome = Chrome().headless(True)
        browser = await chrome.browser()
        page    = (await browser.pages()).pop()
        await page.goto('https://www.google.com/AAAAAA')
        self.png_data = await page.screenshot()

    @sync
    async def test_site__not_headless_what_is_my_browser(self):
        chrome = Chrome(headless=False)
        browser = await chrome.browser()
        page = (await browser.pages()).pop()
        await page.goto('https://www.whatismybrowser.com')
        self.png_data = await page.screenshot()
