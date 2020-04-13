from unittest import TestCase

from syncer import sync

from osbot_browser.browser.Chrome import Chrome
from osbot_utils.utils.Files import temp_file, file_delete, file_contents
from osbot_utils.utils.Http import WS_is_open


class test_Chrome(TestCase):

    def setUp(self) -> None:
        self.chrome = Chrome()

    @sync
    async def test_browser_connect(self):
        chrome = await self.chrome.browser_connect()
        assert WS_is_open(chrome.wsEndpoint)

    def test_get_set_last_chrome_session(self):
        self.chrome.file_tmp_last_chrome_session = temp_file()
        url_chrome = 'ws://127.0.0.1:64979/devtools/browser/75fbaab9-33eb-41ee-afd9-4aed65166791'
        raw_file   = f"""{{
  "url_chrome": "{url_chrome}"
}}"""

            #{ 'url_chrome':}
        self.chrome.set_last_chrome_session(url_chrome)
        assert self.chrome.get_last_chrome_session()                   == url_chrome
        assert file_contents(self.chrome.file_tmp_last_chrome_session) == raw_file

        file_delete(self.chrome.file_tmp_last_chrome_session)

