def setup(event):
    from osbot_browser.browser.Browser_Commands import load_dependencies
    load_dependencies('syncer , requests , pyppeteer')

    from osbot_browser.view_helpers.Sow_Views import Sow
    headless = event.get('headless') is None
    return Sow(headless=headless)

def run(event, context):
    sow = setup(event)
    sow.load_page(reload=True)
    sow.invoke_js('set_data', event.get('issue_data'))
    return sow.api_browser.sync__screenshot_base64()