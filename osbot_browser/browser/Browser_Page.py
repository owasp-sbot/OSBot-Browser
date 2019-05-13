from time import sleep

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper


class Browser_Page:

    def __init__(self,headless=True, new_page=True):
        self.headless        = headless
        self.browser        = None
        self.browser_helper = None
        self.new_page       = new_page
        self.page           = None

    def setup(self):
        self.browser_helper = Browser_Lamdba_Helper(headless=self.headless).setup()
        self.browser        = self.browser_helper.api_browser
        if self.new_page:
            self.page = self.browser.sync__new_page()
        else:
            self.page = self.browser.sync__page()
        return self

    def click(self, element):
        self.browser.sync__click(self.page, element)
        return self

    def close(self):
        self.browser.sync__page_close(self.page)
        return self

    def exists(self,selector):
        return len(self.select(selector)) > 0

    def javascript_eval(self, code):
        return self.browser.sync__js_execute(code, self.page)

    def open(self,url):
        self.browser.sync__open(url,self.page)
        return self

    def width(self, width):
        self.browser.sync__browser_width(width)
        return self

    def select(self, selector):
        return self.browser.sync__query_selector_all(self.page, selector)

    def screenshot(self,url=None, full_page=True, clip=None, delay=None):
        return self.browser.sync__screenshot_base64(url=url, page=self.page, full_page=full_page, clip=clip, delay=delay )

    def text(self):
        return self.browser.sync__page_text()

    def on_dialog__always_accept(self):
        self.browser.sync_on_dialog__always_accept(self.page)
        return self

    def on_request__block_these(self,items_to_block):
        def on_request(request):
            for item in items_to_block:
                if item in request.url:
                    #print('BLOCKED: {0}'.format(request.url))
                    return False
            return True
        self.browser.sync_on_request(self.page, on_request)
        return self

    def type(self,element, value):
        self.browser.sync__type(self.page, element, value)
        return self

    def url(self):
        return self.browser.sync__url()

    def wait(self, seconds):
        sleep(seconds)
        return self

    def wait_for_navigation(self):
        self.browser.sync__wait_for_navigation(self.page)
        return self


