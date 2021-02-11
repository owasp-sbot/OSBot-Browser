from osbot_aws.Dependencies import load_dependencies, load_dependency
from osbot_aws.apis.shell.Lambda_Shell      import lambda_shell
from osbot_aws.decorators.lambda_save_event import lambda_save_event

from osbot_utils.utils.Process         import Process

#@lambda_shell
#@lambda_save_event
def run(event, context=None):
    load_dependencies('syncer,requests,pyppeteer2,websocket-client')
    from osbot_browser.browser.API_Browser import API_Browser


    url = event.get('url')
    #return url
    # error in this line:  Read-only file system: '/home/sbx_user1051
    api_browser = API_Browser().sync__setup_browser()
    # we don't get here

    if url:
        api_browser.sync__open(url)

    return api_browser.sync__screenshot_base64()
    #return api_browser.sync__url()

    #from osbot_browser.browser.Browser_Page import Browser_Page
    #page = Browser_Page().setup()

    #page.open(url)
    #return page.screenshot()
    # return page.text()
    # return page.url(), page.text()