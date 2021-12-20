import base64
from urllib.parse                      import urljoin
from osbot_utils.utils.Dev             import pprint
from osbot_utils.utils.Misc            import list_index_by
from osbot_browser.browser.API_Browser import API_Browser

class Web_Base:

    def __init__(self, target_server, headless=True, api_browser=None, path_screenshot=None, user_agent=None):
        self.api_browser     = api_browser or API_Browser(headless=headless)
        self.user_agent      = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        self.path_screenshot = path_screenshot
        self.target_server   = target_server

    async def cookies(self):
        cookies = await self.cookies_raw()
        return list_index_by(cookies, 'name')

    async def cookies_set(self, cookies):
        page = await self.page()
        await page.setCookie(cookies)

    async def cookies_raw(self):
        return await self.api_browser.page_cookies()

    async def cookies_on_url(self,url):
        page = await self.page()
        return await page._client.send('Network.getCookies', {'urls': [url]})

    async def close_browser(self):
        return await self.api_browser.browser_close()

    async def element(self, selector):
        return await self.api_browser.element(page=await self.page(), selector=selector)

    async def element_type(self, selector, value):
        return await self.api_browser.element_type(page=await self.page(), target=selector, value=value)

    async def element_attributes(self, selector):
        page = await self.page()
        return await self.api_browser.element_attributes(page, selector, index_by_key=True)

    async def element_click(self, selector):
        page = await self.page()
        await self.api_browser.wait_for_element(selector=selector, page=page, visible=True)
        return await self.api_browser.element_click(page=page, target=selector)

    async def element_set_value(self, selector, value):
        js_code = f"document.getElementById('{selector}').value = '{value}'"
        return await self.api_browser.js_eval(code=js_code)

    async def has_element(self, selector):
        return await self.api_browser.element(selector=selector) is not None

    async def html(self, selector=None):                            # todo: figure out a better way to manage the dependencies in a scalable way
        from osbot_browser.py_query.Py_Query import Py_Query        # todo: this is here until we figure out how to run Py_Query/PyQuery in Lambda
        html = await self.html_raw()                                # get raw html from page
        return Py_Query(html=html, selector=selector)               # return Py_Query object

    async def html_raw(self):
        return await self.api_browser.html_raw()

    async def intercept_requests(self, page=None):
        return await self.api_browser.page_capture_requests(page=page)

    async def intercept_responses(self, capture_text=True):
        return await self.api_browser.page_capture_responses(capture_text=capture_text)

    async def open(self, path='', wait_until=None):
        url = urljoin(self.target_server,path)
        page = await self.page()
        try:
            await self.api_browser.open(url=url, page=page, wait_until=wait_until)
        except Exception as error:
            pprint(f'Error in Web_Base - open: {error}')
        return url

    async def open__wait_until__network_idle_0(self, path=''):
        return await self.open(path=path, wait_until='networkidle0')

    async def open__wait_until__network_idle_2(self, path=''):
        return await self.open(path=path, wait_until='networkidle2')

    async def open_capture_requests_and_responses(self, path='', response_capture_text=True):
        requests  = await self.api_browser.page_capture_requests()
        responses = await self.api_browser.page_capture_responses(capture_text=response_capture_text)
        url       = await self.open(path)

        return {'path'      : path      ,
                'url'       : url       ,
                'requests'  : requests  ,
                'responses' : responses }

    async def open_directly(self, url='https://httpbin.org/get'):
        return await self.api_browser.open(url)

    async def page(self):
        page = await self.api_browser.page()
        await page.setUserAgent(self.user_agent);
        return page

    async def screenshot(self, path_screenshot=None):
        path_screenshot = path_screenshot or self.path_screenshot
        return await self.api_browser.screenshot(file_screenshot=path_screenshot)

    async def screenshot_base64(self):
        screenshot_file = await self.screenshot()
        return base64.b64encode(open(screenshot_file, 'rb').read()).decode()

    async def url(self):
        return await self.api_browser.url()

    async def wait_for_element(self, selector):
        return await self.api_browser.wait_for_element(selector=selector)

    async def wait_for_navigation(self):
        await self.api_browser.wait_for_navigation()