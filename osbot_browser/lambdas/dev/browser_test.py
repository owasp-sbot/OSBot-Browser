#@lambda_shell
#@lambda_save_event

from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper

def run(event, context=None):
    headless       = event.get('headless', True)
    url            = event.get('url'     )
    delay          = event.get('delay'   )
    js_code        = event.get('js_code' )
    browser_helper = Browser_Lamdba_Helper(headless).setup()
    png_data       = browser_helper.get_screenshot_png(url       = url    ,
                                                       full_page = True   ,
                                                       delay     = delay  ,
                                                       js_code   = js_code)
    return png_data