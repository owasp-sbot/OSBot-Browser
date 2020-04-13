from unittest import TestCase

from osbot_browser.browser.Chrome import Chrome
from osbot_utils.decorators.Sync import sync
from osbot_utils.testing.Unit_Test import Unit_Test
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import temp_file, file_delete, file_contents
from osbot_utils.utils.Http import WS_is_open, port_is_open


class test_Chrome(Unit_Test):

    def setUp(self):
        super().setUp()
        self.chrome = Chrome()
        self.chrome.headless    = True
        self.chrome.auto_close  = self.chrome.headless is True
        self.chrome.new_browser = True
        self.result             = None

    @sync
    async def test_browser_connect(self):
        browser = await self.chrome.browser_connect()
        assert type(browser).__name__ == 'Browser'
        assert WS_is_open(browser.wsEndpoint)

    # move to separate methods
    @sync
    async def test_open(self):
        browser = await self.chrome.browser()
        url = 'https://www.google.com/404'
        #url = 'https://news.bbc.co.uk'
        #url = 'https://file-drop.co.uk/aaaa'
        page     = await browser.newPage()
        response = await page.goto(url)
        self.result = page.url == url
        png_data = await page.screenshot()
        self.png_data = png_data #(await page.screenshot())



    def test_get_set_last_chrome_session(self):
        self.chrome.file_tmp_last_chrome_session = temp_file()
        url_chrome = 'ws://127.0.0.1:64979/devtools/browser/75fbaab9-33eb-41ee-afd9-4aed65166791'
        raw_file   = f"""{{
  "url_chrome": "{url_chrome}"
}}"""
        self.chrome.set_last_chrome_session(url_chrome)
        assert self.chrome.get_last_chrome_session()                   == url_chrome
        assert file_contents(self.chrome.file_tmp_last_chrome_session) == raw_file
        file_delete(self.chrome.file_tmp_last_chrome_session)



    # utils methods
    @sync
    async def test_browser(self):
        browser = await self.chrome.browser()
        assert type(browser).__name__ == 'Browser'

        # '/Users/diniscruz/Library/Application Support/pyppeteer/local-chromium/588429/chrome-mac/Chromium.app/Contents/MacOS/Chromium'

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

    @sync
    async def test_version(self):
        assert await self.chrome.version() == 'HeadlessChrome/71.0.3542.0'

    @sync
    async def test_ws_endpoint(self):
        assert WS_is_open(await self.chrome.ws_endpoint())

    # Use case tests

    @sync
    async def test_confirm_chrome_starts_in_new_process(self):
        pid_1 = (await Chrome().browser()).process.pid
        pid_2 = (await Chrome().browser()).process.pid
        assert pid_1 > 10
        assert pid_1 != pid_2