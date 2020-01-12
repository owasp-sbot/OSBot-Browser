from osbot_browser.browser.Browser_Page import Browser_Page



def run(event, context):
    headless = event.get('headless') is None
    web_root = event.get('web_root')
    page     = event.get('page')
    js_code  = event.get('js_code')

    from osbot_browser.browser.Browser_Commands import load_dependencies
    load_dependencies('syncer , requests , pyppeteer')


    from osbot_browser.browser.API_Browser import API_Browser
    from osbot_browser.browser.Render_Page import Render_Page
    from osbot_browser.browser.Web_Server import Web_Server

    api_browser = API_Browser(headless=headless).sync__setup_browser()
    web_server  = Web_Server(web_root)
    render_page = Render_Page(api_browser=api_browser, web_server=web_server)

    render_page.open_file_in_browser(page)

    if js_code:
        api_browser.sync__js_execute(js_code)

    return api_browser.sync__screenshot_base64()



























    # from osbot_browser.view_helpers.Sow_Views import Sow
    # params = {}
    # maps = Sow(headless=False)
    # maps.load_page(True)
    #
    # issue_data = {
    #     "requirement_number": "1A - Determine File Type",
    #     "requirement_language": "N/A",
    #     "verification_method": "Test",
    #     "setup": "",
    #     "execution_steps": "<ol><li></li><li></li><li></li><li></li><li></li></ol>",
    #     "expected_result": '',
    #     "compliance": '&lt;Compliant | Partially Compliant | Non-Compliant &gt;',
    #     "results": "{0}".format(params)
    # }
    # maps.invoke_js('set_data', issue_data)

    #return { 'png_file': maps.create_dashboard_screenshot() }