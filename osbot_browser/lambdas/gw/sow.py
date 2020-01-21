from osbot_aws.apis.Lambda import Lambda

def setup(event):
    from osbot_browser.browser.Browser_Commands import load_dependencies
    load_dependencies('syncer , requests , pyppeteer , jira')

    from osbot_browser.view_helpers.Sow_Views import Sow
    headless = event.get('headless') is None
    return Sow(headless=headless)

def get_issue_data(jira_id):
    jira_data = Lambda('osbot_jira.lambdas.gw.gw_jira').invoke({"issue_id": jira_id})
    if jira_data is None:
        return {}

    enhancement_id     = jira_data.get('EnhancementId')
    title              = jira_data.get('Summary')
    description         = jira_data.get('Description')
    setup               = jira_data.get('Setup')
    verification_method = jira_data.get('Verification Method')
    execution_steps     = jira_data.get('Execution Steps')
    expected_result     = jira_data.get('Expected Results')
    status              = jira_data.get('Status')
    issue_links         = jira_data.get('Issue Links')
    results             = jira_data.get('Actual results')

    issue_data = {
        "requirement_number"    : enhancement_id,
        "requirement_language"  : title,
        "verification_method"   : verification_method,
        "setup"                 : setup,
        "execution_steps"       : execution_steps,
        "expected_result"       : expected_result,
        "compliance"            : f'{status}-' ,
        "results"               : results ,
        "issue_links"           : f'{issue_links}' ,
        "jira_id"               : jira_id
    }
    return issue_data

def run(event, context):
    sow        = setup(event)
    issue_data = get_issue_data(event.get('issue_id'))
    sow.load_page(reload=True)
    sow.invoke_js('set_data', issue_data)
    return sow.api_browser.sync__screenshot_base64()