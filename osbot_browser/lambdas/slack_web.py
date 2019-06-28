from osbot_aws.apis.Lambda import load_dependency


def run(event, context):
    load_dependency('syncer')

    target = event.get('target')
    channel  = event.get('channel')
    team_id  = event.get('team_id')
    width    = event.get('width')
    height   = event.get('height')
    if width is None:
        width = 1200
    if height is None:
        height = 1000

    from osbot_browser.browser.sites.Web_Slack import Web_Slack

    web_slack = Web_Slack(team_id=team_id).setup()

    web_slack.login()
    web_slack.page.width(width, height)

    if target:
         web_slack.open(target)

    web_slack.fix_ui_for_screenshot()
    png_data =  web_slack.screenshot()
    return png_data