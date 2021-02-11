import sys ;

import pytest
from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.utils import Misc
from osbot_utils.utils.Files import Files, file_open
from osbot_utils.utils.Process import exec_open

from osbot_browser.Deploy import Deploy

sys.path.append('../osbot_browser')

import base64
from syncer import sync
from unittest import TestCase

from osbot_browser.browser.API_Browser                import API_Browser


class test_API_Browser(TestCase):

    def setUp(self):
         self.api = API_Browser(headless = False)

    #@unittest.skip("bug: needs to load markdow page first")
    @sync
    async def test_js_eval(self):
        text = "some_text"
        text_base64 = base64.b64encode(text.encode()).decode()
        assert await self.api.js_eval("btoa('{0}')".format(text))        == text_base64
        assert await self.api.js_eval("atob('{0}')".format(text_base64)) == text

    @sync
    async def test_html(self):
        await self.api.open('https://www.google.com')
        html = await self.api.html()
        assert len(html) > 100

    @sync
    async def test_open(self):
        (headers, status, url, browser) = await self.api.open('https://www.google.com')
        assert headers['x-frame-options'] == 'SAMEORIGIN'
        assert status                     == 200
        assert url                        == 'https://www.google.com/'

    @sync
    async def test_page(self):
        url = 'https://www.google.com/404'
        await self.api.open(url)
        page = await self.api.page()
        assert page.url == url


    @sync
    async def test_screenshot(self):
        await self.api.open('https://news.bbc.co.uk')
        file_jpg = await self.api.screenshot()
        assert Files.exists(file_jpg)
        #exec_open(file_jpg)

    @sync
    @pytest.mark.skip("needs to run in Headless mode")
    async def test_pdf(self):
        # note: only works when headless = True . See https://github.com/puppeteer/puppeteer/issues/1829#issuecomment-657930419
        await self.api.open('https://news.bbc.co.uk')
        file_pdf = await self.api.pdf()
        assert Files.exists(file_pdf)
        exec_open(file_pdf)

    def test_open_settings(self):
        page = 'chrome://settings/help'
        self.api.sync__open(page)
