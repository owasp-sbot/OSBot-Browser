import sys ; sys.path.append('../osbot_browser')

import base64
import unittest
from syncer import sync
from unittest import TestCase

from osbot_browser.browser.API_Browser                import API_Browser
from pbx_gs_python_utils.utils.Dev      import Dev
from pbx_gs_python_utils.utils.Files    import Files
from pbx_gs_python_utils.utils.Http     import WS_is_open


class test_API_Browser(TestCase):

    def setUp(self):
         self.api = API_Browser(headless = False)

    @sync
    async def test_browser_connect(self):
        browser = await self.api.browser_connect()
        assert WS_is_open(browser.wsEndpoint)

    def test_get_set_last_chrome_session(self):
        self.api.file_tmp_last_chrome_session = Files.temp_file()
        data = { 'chrome_devtools':'ws://127.0.0.1:64979/devtools/browser/75fbaab9-33eb-41ee-afd9-4aed65166791'}
        self.api.set_last_chrome_session(data)
        assert self.api.get_last_chrome_session() == data
        Files.delete(self.api.file_tmp_last_chrome_session)

    @unittest.skip("bug: needs to load markdow page first")
    @sync
    async def test_js_eval(self):
        markdown = """
# some title "with double quotes"
some text  and 'single quotes'
"""
        encoded_text = base64.b64encode(markdown.encode()).decode()
        js_script = "convert(atob('{0}'))".format(encoded_text)

        result = await self.api.js_eval(js_script)
        #Dev.pprint(result)

    @unittest.skip("bug: needs to load markdow page first")
    @sync
    async def test_invoke_js_function(self):
        markdown = """
# changed title "via js function"
some text  and 'single quotes'
"""
        result = await self.api.js_invoke_function('convert',markdown)
        #Dev.pprint(result)

    @sync
    async def test_html(self):
        await self.api.open('https://www.google.com')
        content = await self.api.html()
        assert len(content.html()) > 100

    @sync
    async def test_open(self):
        (headers, status, url, browser) = await self.api.open('https://www.google.com')
        assert headers['x-frame-options'] == 'SAMEORIGIN'
        assert status                     == 200
        assert url                        == 'https://www.google.com/'

    @sync
    async def test_page(self):
        page = await self.api.page()
        assert "http" in page.url


    @sync
    async def test_screenshot(self):
        await self.api.open('https://news.bbc.co.uk')
        file = await self.api.screenshot()
        assert Files.exists(file)


class test_workflows_API_Browser(TestCase):


    @sync
    async def test_open_jira_page(self):
        from osbot_aws.apis.Secrets import Secrets
        self.api = API_Browser(headless=False)

        login_needed = False
        self.secrets_id = 'GS_BOT_GS_JIRA'

        (server, username, password) = Secrets(self.secrets_id).value_from_json_string().values()

        if login_needed:
            Dev.pprint(server, username, password)
            await self.api.open(server + '/login.jsp')
            page = await self.api.page()
            await page.type('#login-form-username', username)
            await page.type('#login-form-password', password)
            await page.click('#login-form-submit')

        #await self.api.open(server + '/browse/GSP-95')
        #page = await self.api.page()
        #await self.api.js_execute("$('#show-more-links-link').click()")
        #from time import sleep
        #sleep(1)
        await self.api.page_size(2000,3000)

        await self.api.screenshot(file_screenshot='/tmp/tmp-jira-screenshot.png', full_page=True)



class Test_API_Browser___with_browser_not_closing(TestCase):

    def setUp(self):
        self.api = API_Browser(headless=True)

    @sync
    async def test_html(self):
        await self.api.open('https://www.google.co.uk')
        content = await self.api.html()
        assert "Google" in content.html()