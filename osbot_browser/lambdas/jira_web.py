from osbot_aws.apis.Lambda import load_dependency


def run(event, context):

    load_dependency('syncer')
    from osbot_browser.browser.sites.Web_Jira import Web_Jira
    web_jira = Web_Jira().setup()
    web_jira.login()
    web_jira.issue('RISK-12')
    return web_jira.screenshot()