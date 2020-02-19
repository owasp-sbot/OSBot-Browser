


def run(event, context):
    try:
        from osbot_aws.Dependencies import load_dependencies
        load_dependencies('syncer,requests,pyppeteer')
        from osbot_browser.view_helpers.gw.Xml_Report import Xml_Report

        headless  = event.get('headless')
        file_name = event.get('file_name')
        json_data = event.get('json_data')

        png_data  = Xml_Report(headless=headless).gw_exec_summary(file_name, json_data)
        return {'png_data': png_data }
    except Exception as error:
        return {'error': f'{error}'}