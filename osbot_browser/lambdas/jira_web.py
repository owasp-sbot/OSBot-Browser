from pbx_gs_python_utils.utils.Misc import Misc
from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.Dependencies import load_dependencies
from time import sleep

from osbot_aws.apis.shell.Lambda_Shell              import lambda_shell
from osbot_browser.browser.Browser_Lamdba_Helper    import Browser_Lamdba_Helper


@lambda_shell
def run(event, context):

    issue_id = event.get('issue_id')
    channel  = event.get('channel')
    team_id  = event.get('team_id')
    width    = event.get('width')
    height   = event.get('height')
    delay    = Misc.to_int(event.get('delay'))
    headless = event.get('headless', True)

    if issue_id is None:
        return { 'error': 'No issue ID provided' }

    Browser_Lamdba_Helper().load_browser_dependencies()

    #load_dependencies('syncer,requests,pyppeteer,websocket-client')
    try:
        from osbot_browser.browser.sites.Web_Jira import Web_Jira
        web_jira = Web_Jira(headless=headless).setup()


        slack_message(':one: Logging in...', [] ,channel)
        web_jira.login()
        #return web_jira.screenshot()

        slack_message(f':two: opening issue `{issue_id}` in headless chrome', [], channel)
        web_jira.issue(issue_id)

        if width is None:
            width = 1200
        if height is None:
            height = 300
        if delay:
            slack_message(f':hourglass: Pausing for {delay} seconds before taking the screenshot',[],channel)
            sleep(delay)

        web_jira.fix_issue_remove_ui_elements()

        #todo: next line breaks when delay is too big (need to find a way to keep the browser alive)

        png_data = web_jira.screenshot(width, height)

        if channel:
            title = "Issue: {0}".format(issue_id)
            slack_message(f':three: sending screenshot to slack image with size {len(png_data)}', [], channel)
            Browser_Lamdba_Helper().send_png_data_to_slack(team_id, channel, title, png_data)
            #return "sent png to slack"

    except Exception as error:
        message = f'Error in jira_web lambda: {error}'
        slack_message(message,[],channel)
        return message
    return png_data