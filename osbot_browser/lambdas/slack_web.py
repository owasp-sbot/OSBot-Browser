


def run(event, context):
    from oss_bot.lambdas.png_to_slack import load_dependency
    load_dependency('syncer')
    load_dependency('requests')
    load_dependency('pyppeteer')

    from pbx_gs_python_utils.utils.Lambdas_Helpers   import slack_message
    from osbot_browser.browser.sites.Web_Slack       import Web_Slack
    from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper

    target    = event.get('target')
    channel   = event.get('channel')
    team_id   = event.get('team_id')
    width     = event.get('width')
    height    = event.get('height')
    scroll_by = event.get('scroll_by')
    delay     = event.get('delay')

    try:
        if width is None : width = 1200
        if height is None: height = 1000

        web_slack = Web_Slack(team_id=team_id).setup()

        web_slack.login()
        web_slack.page.width(width, height)

        if target   : web_slack.open(target)
        if scroll_by: web_slack.scroll_messages_by(scroll_by)
        if delay    : web_slack.wait(delay)

        web_slack.fix_ui_for_screenshot()
        png_data =  web_slack.screenshot()
        slack_message(':information_source: got screenshot with size `{0}` | :point_right: sending screeenshot to slack channel `{1}`'.format(len(png_data), channel), [], channel=channel, team_id=team_id)
        browser_helper = Browser_Lamdba_Helper()
        return browser_helper.send_png_data_to_slack(team_id, channel, target, png_data)
    except Exception as error:
        return slack_message(':red_circle: Error in `slack_web` lambda: {0}'.format(error), [], channel=channel,team_id=team_id )