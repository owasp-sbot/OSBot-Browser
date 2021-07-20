import asyncio
import base64
import json

from pyppeteer.element_handle import ElementHandle
from syncer import sync

from osbot_browser.chrome.Chrome import Chrome
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files

# see https://github.com/puppeteer/puppeteer/blob/master/docs/api.md for all the functions available

class API_Browser:

    def __init__(self, browser=None, headless=True):  # headless = True, new_browser=False, url_chrome = None):
        self.file_tmp_screenshot          = Files.temp_file('.png')
        self.file_tmp_pdf                 = Files.temp_file('.pdf')
        self._browser                     = browser
        self.headless                     = headless
        self.log_js_errors_to_console     = True

    async def browser(self):
        if self._browser is None:
            self._browser = await Chrome(self.headless).browser()
        return self._browser

    async def browser_close(self):
        browser = await self.browser()
        if browser is not None:
            pages = await browser.pages()
            for page in pages:              # not sure if this makes any difference
               await page.close()
            await browser.close()

    async def element(self, page, selector):
        if type(selector) is ElementHandle:      # for the cases when a selector is already a selector
            return selector                     # todo: add better check that it is a selector
        try:
            return await page.querySelector(selector)
        except:
            return None

    async def element_attribute(self, page, target, name):
        element = await self.element(page, target)
        if element:
            return await page.evaluate('(element, name) => element.getAttribute(name)', element, name)

    async def element_attributes(self, page, target):
        element = await self.element(page, target)
        if element:
            return await page.evaluate('(element) => element.getAttributeNames().map((name)=>  { return { [name]: element.getAttribute(name) } } )', element)

    async def element_click(self, page, target):
        element = await self.element(page=page, selector=target)
        if element:
            await element.click()


    async def element_property(self, page, target, property):
        element = await self.element(page, target)
        if element:
            return await page.evaluate(f'(element) => element.{property}', element)
        return None

    async def element_type(self, page, target, value):
        element = await self.element(page=page, selector=target)
        if element:
            await element.type(value)

    async def elements(self, page, target):
        if type(target) is list:             # cases when target is a list of elements
            return target
        try:
            return await page.querySelectorAll(target)
        except:
            return None

    async def elements_attribute(self, page, selector, name):
        result = []
        elements = await self.elements(page, selector)
        if elements:
            for element in elements:
                result.append(await self.element_attribute(page, element, name))
        return result

    async def elements_attributes(self, page, selector):
        result = []
        for element in await self.elements(page, selector):
            result.append(await self.element_attributes(page, element))
        return result

    async def elements_property(self, page, selector, property):
        result = []
        for element in await self.elements(page, selector):
            result.append(await self.element_property(page, element, property))
        return result

    async def js_execute(self, js_code,page=None):
        if js_code:
            if type(js_code).__name__ == 'str':                              # if it is a string, execute it
                return await self.js_eval(js_code,page=page)

            if type(js_code).__name__ == 'list':                             # if it is an list (i.e. array)
                list_types = [type(item).__name__ for item in js_code]       # get all array items type
                all_string = list(set(list_types)) == ['str']                # get unique list and check if all are string
                if all_string:                                               # if they are
                    js_code = ";\n".join(js_code)                            # join them all (separated by ;)
                    return await self.js_eval(js_code,page=page)                       # execute it

            name   = js_code.get('name')                                     # if js_code was an object
            params = js_code.get('params'  )                                 # get the name and params values
            if name and params:
                return await self.js_invoke_function(name, params,page=page) # execute them as a js method

    async def js_eval(self, code,page=None):
        if page is None:
            page = await self.page()
        try:
            return await page.evaluate(code)
        except Exception as error:
            error_message = "[js eval error]: {0}".format(error)
            if self.log_js_errors_to_console:
                print(error_message)
            return error_message

    async def js_invoke_function(self, name, params=None,page=None):
        if params:
            if type(params).__name__ != 'str':
                params = json.dumps(params)
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0}(JSON.parse(atob('{1}')))".format(name, encoded_text )
            else:
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0}(atob('{1}'))".format(name, encoded_text)
        else:
            js_script = "{0}()".format(name)
        return await self.js_eval(js_script,page=page)

    async def js_assign_variable(self, variable, data=None, page=None):
        if data:
            if type(data).__name__ != 'str':
                params = json.dumps(data)
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0} = JSON.parse(atob('{1}'))".format(variable, encoded_text )
            else:
                encoded_text = base64.b64encode(data.encode()).decode()
                js_script = "{0} = atob('{1}')".format(variable, encoded_text)
        else:
            js_script = "{0} = undefined".format(variable)
        return await self.js_eval(js_script,page=page)

    async def open(self, url, wait_until=None, page=None):
        if page is None:
            page = await self.page()
        if wait_until:
            response  = await page.goto(url, waitUntil= wait_until)  # returns response object
        else:
            response = await page.goto(url)

        if response:
            headers   = response.headers
            status    = response.status
            url       = response.url
            return headers, status, url, self
        return None, None, url, self

    async def new_page(self):
        browser = await self.browser()
        return await browser.newPage()

    async def page(self):
        browser = await self.browser()
        pages = await browser.pages()
        page = pages.pop()
        return page

    async def page_cookies(self):
        page = await self.page()
        return await page.cookies()

    # todo: add suport for
    #       in setup code:
    #           await page.setRequestInterception(True);
    #       inside the intercept_request(request) method
    #           await request.continue_({'url': 'http://tarhet'})

    async def page_capture_requests(self, page=None, on_request=None):
        requests = []

        async def intercept_request(request):
            properties_to_capture = ['headers', 'method', 'postData', 'redirectChain', 'resourceType','url']
            request_data          =  {}
            for property_to_capture in properties_to_capture:
                request_data[property_to_capture] = getattr(request, property_to_capture)
            request_data['frame_name'] = request.frame.name
            requests.append(request_data)

            if on_request:
                on_request(request_data)
        if page is None:
            page = await self.page()

        page.on('request', lambda request: asyncio.ensure_future(intercept_request(request)))

        return requests

    async def page_capture_responses(self, page=None, on_response=None):
        responses = []

        async def intercept_response(response):
            response_data = {}
            try:
                properties_to_capture = ['fromCache', 'headers', 'ok', 'status', 'url']
                for property_to_capture in properties_to_capture:
                    response_data[property_to_capture] = getattr(response, property_to_capture)
                response_data['request_frame_name'] = response.request.frame.name
                response_data['request_headers'   ] = response.request.headers
                response_data['request_method'    ] = response.request.method
                response_data['request_post_data' ] = response.request.postData
                response_data['headers'           ] = response.headers

                if 'text' in response.headers.get('content-type'):
                    response_data['text'] = await response.text()
            except Exception as error:
                response_data['intercept_response_error'] = error
                response_data['text'] = ''

            responses.append(response_data)

            if on_response:
                on_response(response_data)
        if page is None:
            page = await self.page()

        page.on('response'                         , lambda response: asyncio.ensure_future(intercept_response(response)))

        return responses

    async def pages(self):
        browser = await self.browser()
        return await browser.pages()

    async def sleep(self, mseconds):
        page = await self.page()
        await page.waitFor(mseconds)
        return self

    async def html(self):
        return await self.html_raw()
        # try:
        #     from pyquery import PyQuery         # add it here since there was some import issues with running it in lambda (etree). Also this method should not be that useful inside an lambda
        #     content = await self.html_raw()
        #     return PyQuery(content)
        # except:
        #     return await self.html_raw()

    async def html_raw(self):
        page = await self.page()
        return await page.content()

    # todo: refactor pdf and screenshot methods since most of the code is the same
    async def pdf(self, url= None, page=None, full_page = True, file_pdf = None, clip=None, viewport=None, js_code=None, delay=None):
        if url:
            await self.open(url,page=page)

        await self.js_execute(js_code)

        if delay:
            await asyncio.sleep(delay)

        if file_pdf is None:
            file_pdf = self.file_tmp_pdf

        page = await self.page()
        if viewport:
            await self.viewport(viewport)
        if clip:
            full_page = False
        await page.pdf({'path': file_pdf,'fullPage': full_page, 'clip' : clip})

        return file_pdf

    async def screenshot(self, url= None, page=None, full_page = True, file_screenshot = None, clip=None, viewport=None, js_code=None, delay=None):
        if url:
            await self.open(url,page=page)

        await self.js_execute(js_code)

        if delay:
            await asyncio.sleep(delay)

        if file_screenshot is None:
            file_screenshot = self.file_tmp_screenshot

        page = await self.page()
        if viewport:
            await self.viewport(viewport)
        if clip:
            full_page = False
        await page.screenshot({'path': file_screenshot,'fullPage': full_page, 'clip' : clip})

        return file_screenshot

    async def url(self):
        page = await self.page()
        return page.url

    async def page_size(self, width, height):
        page = await self.page()
        await page.setViewport({'width': width, 'height': height})
        return self

    async def viewport(self, viewport):
        page = await self.page()
        await page.setViewport(viewport)
        return self

    async def xpath(self, page, xpath, return_error=False):
        try:
            return await page.xpath(xpath)
        except Exception as error:
            if return_error:
                return {'error': error}
            return None


    async def wait_for_element(self, selector, timeout=10000,page=None, visible=False ,hidden=False):
        if page is None:
            page = await self.page()
        try:
            await page.waitForSelector(selector, {'timeout': timeout ,'visible':visible, 'hidden': hidden})
            return True
        except Exception as error:
            Dev.pprint("[Error][sync__await_for_element] {0}".format(error))
            return False

    async def wait_for_navigation(self, page=None):
        if page is None:
            page = await self.page()
        await page.waitForNavigation()
        return self

    # helper sync functions
    @sync
    async def sync__browser_width(self, width,height=None):
        if height is None: height = width
        return await self.page_size(width, height)

    @sync
    async def sync__click(self,page, element):
        await page.click(element)
        return self

    @sync
    async def sync__close_browser(self):
        await self._browser.close()
        return self

    @sync
    async def coverage_start(self, page):
        await page.coverage.startJSCoverage()
        await page.coverage.startCSSCoverage()

    @sync
    async def coverage_stop(self, page):
        js_coverage = await page.coverage.stopJSCoverage()
        css_coverage = await page.coverage.stopCSSCoverage()
        return {'js_coverage': js_coverage, 'css_coverage': css_coverage}

    @sync
    async def sync__element(self, page, selector):
        return await self.element(page, selector)

    @sync
    async def sync__element_attribute(self, page, selector, name):
        return await self.element_attribute(page, selector, name)

    @sync
    async def sync__element_attributes(self, page, selector):
        return await self.element_attributes(page, selector)

    @sync
    async def sync__element_html_inner(self, page, selector):
        return await self.element_property(page, selector, 'innerHTML')

    @sync
    async def sync__element_html_outer(self, page, selector):
        return await self.element_property(page, selector, 'outerHTML')

    @sync
    async def sync__element_property(self, page, selector, property):
        return await self.element_property(page, selector, property)

    @sync
    async def sync__element_text(self, page, selector):
        return await self.element_property(page, selector, 'textContent')

    @sync
    async def sync__elements_attribute(self, page, selector, name):
        return await self.elements_attribute(page, selector, name)

    @sync
    async def sync__elements_attributes(self, page, selector):
        return await self.elements_attributes(page, selector)

    @sync
    async def sync__elements_html_inner(self, page, selector):
        return await self.elements_property(page, selector, 'innerHTML')

    @sync
    async def sync__elements_html_outer(self, page, selector):
        return await self.elements_property(page, selector, 'outerHTML')

    @sync
    async def sync__elements_property(self, page, selector, property):
        return await self.elements_property(page, selector, property)

    @sync
    async def sync__elements_text(self, page, selector):
        return await self.elements_property(page, selector, 'textContent')

    @sync
    async def sync__elements_xpath(self, page, xpath, return_error=False):
        return await self.xpath(page, xpath,return_error)

        #return await self.elements_property(page, selector, 'textContent')
    @sync
    async def sync__js_execute(self, js_code,page=None):
        return await self.js_execute(js_code,page=page)

    @sync
    async def sync_js_invoke_function(self,name, params=None,page=None):
        return await self.js_invoke_function(name, params,page=page)

    @sync
    async def sync_js_assign_variable(self, variable, data=None, page=None):
        return await self.js_assign_variable(variable,data,page=page)

    @sync
    async def sync__html_raw(self):
        return await self.html_raw()

    @sync
    async def sync__new_page(self):
        return await self.new_page()

    @sync
    async def sync_on_dialog__always_accept(self,page):

        async def close_dialog(dialog):
            print("on close_dialog: {0}".format(dialog))
            await dialog.accept()

        page.on('dialog', lambda dialog: close_dialog(dialog))
        return page

    @sync
    async def sync_on_request(self, page, on_request):
        async def on_request_local_handler(request):
            if on_request and on_request(request):
                return await request.continue_()
            else:
                return await request.abort()

        await page.setRequestInterception(True)
        page.on('request', lambda dialog: on_request_local_handler(dialog))
        return page

    @sync
    async def sync__page(self):
        return await self.page()

    @sync
    async def sync__pages(self):
        return await self.pages()

    @sync
    async def sync__page_close(self,page):
        return await page.close()

    @sync
    async def sync__page_text(self, page=None):
        if page is None:
            page = await self.page()
        return await page.evaluate('() => document.body.innerText')

    # @sync
    # async def sync__page__with_auto_dialog_accept(self):
    #     page = await self.page()
    #
    #     async def close_dialog(dialog):
    #         print("on close_dialog: {0}".format(dialog))
    #         await dialog.accept()
    #
    #     #page.on('dialog', lambda dialog: asyncio.ensure_future(close_dialog(dialog)))
    #     page.on('dialog', lambda dialog: close_dialog(dialog))
    #     return page

    @sync
    async def sync__open(self, url, page=None):
        await self.open(url,page=page)
        return self

    @sync
    async def sync__type(self,page,element,value):
        await page.type(element,value)
        return self

    @sync
    async def sync__url(self):
        return await self.url()

    @sync
    async def sync__setup_browser(self):
        await self.browser()
        return self
    @sync
    async def sync__screenshot(self, url=None, page=None, file_screenshot = None,clip=None,full_page=True):
        return await self.screenshot(url,page=page, file_screenshot = file_screenshot,clip=clip,full_page=full_page)

    @sync
    async def sync__screenshot_base64(self, url=None, page=None, full_page=True, clip=None,delay=None, js_code=None):
        screenshot_file = await self.screenshot(url=url,page=page, full_page=full_page, clip=clip, delay=delay, js_code=js_code)
        return base64.b64encode(open(screenshot_file, 'rb').read()).decode()

    @sync
    async def sync__await_for_element(self, selector, timeout=10000,page=None, visible=False ,hidden=False):
        return await self.wait_for_element(selector=selector, timeout=timeout, page=page, visible=visible ,hidden=hidden)


    @sync
    async def sync__set_upload_file(self, page, selector, file_path):
        file_element = await self.element(page, selector)
        return await file_element.uploadFile(file_path)


    @sync
    async def sync__wait_for_selector(self, page, selector):
        await page.waitForSelector(selector)
        return self

    @sync
    async def sync__wait_for_navigation(self, page=None):
        return self.wait_for_element(page=page)



    @sync
    async def sync_sleep(self, mili_seconds):
        await self.sleep(mili_seconds)
        return self
