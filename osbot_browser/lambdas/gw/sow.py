def run(event, context):
    return 'hello from lambda 123'


















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

    return { 'png_file': maps.create_dashboard_screenshot() }