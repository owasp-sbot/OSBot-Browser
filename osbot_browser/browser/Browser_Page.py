from time import sleep

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper


class Browser_Page:

    def __init__(self,headless=True, new_page=True):
        self.headless        = headless
        self.browser        = None
        self.browser_helper = None
        self.new_page       = new_page
        self.page           = None

    def setup_with_dependencies(self):
        from osbot_browser.browser.Browser_Commands import load_dependency
        load_dependency('syncer')
        load_dependency('requests')
        load_dependency('pyppeteer')
        return self.setup()

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

    def width(self, width, height=None):
        self.browser.sync__browser_width(width,height)
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

    #document.getElementsByClassName('c-message__bodya').length
    ## NOTE: One solution to handle the probs caused by Session/Page timeout is to reconnect to the browser  (need to check if the reconnect works in AWS)
    #          self.browser.sync__setup_browser()
    #          #self.page = self.browser.sync__page()
    def wait_for_element__class_name(self, element_id, exists=True,wait_for=0.25, max_attempts=20):
        for i in range(0,max_attempts):
            if exists:
                result = self.javascript_eval("document.getElementsByClassName('{0}').length > 0".format(element_id))
            else:
                result = self.javascript_eval("document.getElementsByClassName('{0}').length == 0".format(element_id))
            #print('wait_for_element__class_name',element_id, exists, i, result)
            if result:
                return True
            sleep(wait_for)
        return False

    def wait_for_element__id(self, element_id, exists=True, wait_for=0.25, max_attempts=20):
        for i in range(0,max_attempts):
            if exists:
                result = self.javascript_eval("document.getElementById('{0}') != null".format(element_id))
            else:
                result = self.javascript_eval("document.getElementById('{0}') == null".format(element_id))
            #print('wait_for_element_by_id',element_id, exists, i, result)
            if result:
                return True
            sleep(wait_for)
        return False
        #return self.browser.sync__await_for_element(element, page=self.page,visible=visible, hidden=hidden)

    def wait_for_element__tag_name(self, element_id, exists=True, wait_for=0.25, max_attempts=20):
        for i in range(0,max_attempts):
            if exists:
                result = self.javascript_eval("document.getElementsByTagName('{0}').length > 0".format(element_id))
            else:
                result = self.javascript_eval("document.getElementsByTagName('{0}').length == 0".format(element_id))
            #print('wait_for_element__getElementsByTagName',element_id, exists, i, result)
            if result:
                return True
            sleep(wait_for)
        return False



    def wait_for_jQuery(self, wait_for=0.25, max_attempts=20):
        for i in range(0,max_attempts):
            result = self.javascript_eval("typeof(jQuery)")
            print(i, result)
            if result == 'function':
                return True
            sleep(wait_for)
        return False



