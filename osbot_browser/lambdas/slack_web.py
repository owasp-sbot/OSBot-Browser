


def run(event, context):
    from oss_bot.lambdas.png_to_slack import load_dependency
    load_dependency('syncer')
    load_dependency('requests')
    load_dependency('pyppeteer')

    target    = event.get('target')
    channel   = event.get('channel')
    team_id   = event.get('team_id')
    width     = event.get('width')
    height    = event.get('height')
    scroll_by = event.get('scroll_by')
    delay     = event.get('delay')

    if width is None : width = 1200
    if height is None: height = 1000

    from osbot_browser.browser.sites.Web_Slack import Web_Slack

    web_slack = Web_Slack(team_id=team_id).setup()

    web_slack.login()
    web_slack.page.width(width, height)

    if target   : web_slack.open(target)
    if scroll_by: return web_slack.scroll_messages_by(scroll_by)
    if delay    : web_slack.wait(delay)

    #web_slack.fix_ui_for_screenshot()
    png_data =  web_slack.screenshot()
    return png_data