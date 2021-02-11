from osbot_browser.chrome.Chrome_Sync import Chrome_Sync
from osbot_utils.testing.Unit_Test import Unit_Test


class test_Chrome_Sync(Unit_Test):
    def setUp(self):
        super().setUp()
        self.chrome = Chrome_Sync()

    def test_browser(self):
        assert type(self.chrome.browser()).__name__ == 'Browser'

    def test_close(self):
        self.chrome.close()
        self.assertRaises(Exception, self.chrome.url)

    def test_open__url(self):
        url = 'https://www.google.com/404'
        self.chrome.open(url)
        assert self.chrome.url() == url

    def test_screenshot(self):
        self.png_data = self.chrome.open('https://www.google.com/404').screenshot()