from osbot_aws.apis.Lambda import load_dependency




def run(event, context):
    load_dependency('syncer')
    from osbot_browser.browser.sites.Web_Jira import Web_Jira

    issue_id = event.get('issue_id')
    channel = event.get('channel')
    team_id = event.get('team_id')

    web_jira = Web_Jira().setup()

    web_jira.login()  #web_jira.fix_set_list_view()
    web_jira.issue(issue_id)
    png_data =  web_jira.screenshot(width=1200)

    if channel:
        from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
        title = "Issue: {0}".format(issue_id)
        Browser_Lamdba_Helper().send_png_data_to_slack(team_id, channel, title, png_data)
        return "send png to slack"

    return png_data