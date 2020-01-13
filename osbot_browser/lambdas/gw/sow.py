from osbot_aws.apis.Lambda import Lambda

def setup(event):
    from osbot_browser.browser.Browser_Commands import load_dependencies
    load_dependencies('syncer , requests , pyppeteer , jira')

    from osbot_browser.view_helpers.Sow_Views import Sow
    headless = event.get('headless') is None
    return Sow(headless=headless)

def get_issue_data(jira_id):
    jira_data = Lambda('osbot_jira.lambdas.gw.gw_jira').invoke({"issue_id": jira_id})

    enhancement_id  = jira_data.get('EnhancementId')
    title           = jira_data.get('Summary')
    description     = jira_data.get('Description')
    status          = jira_data.get('Status')
    issue_links     = jira_data.get('Issue Links')

    issue_data = {
        "requirement_number"    : f"{enhancement_id} - {title}",
        "requirement_language"  : "",
        "verification_method"   : "Test",
        "setup"                 : f"{issue_links}",
        "execution_steps"       : f'{description}',
        "expected_result"       : '',
        "compliance"            : f'&lt;Compliant | Partially Compliant | Non-Compliant &gt;',
        "results"               : f'{status}'
    }
    return issue_data

def run(event, context):
    sow        = setup(event)
    issue_data = get_issue_data(event.get('issue_id'))
    sow.load_page(reload=True)
    sow.invoke_js('set_data', issue_data)
    return sow.api_browser.sync__screenshot_base64()