from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.Dependencies import load_dependencies
from osbot_browser.browser.sites.Web_AWS import Web_AWS


def run(event, context):
    load_dependencies('syncer,requests,pyppeteer,websocket-client')
    from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper


    channel = event.get('channel')

    try:
        wait = 3
        aws      = Web_AWS().setup()
        slack_message(':one: Logging in to AWS',[], channel)
        aws.login()

        slack_message(f':two: Opening Billing page and waiting {wait} seconds for data to load',[], channel)
        aws.page_billing()
        aws.page.wait(wait)
        png_data = aws.screenshot(width=1200)

        if channel:
            slack_message(f':three: sending screenshot of size {len(png_data)} to Slack channel {channel}',[], channel)
            Browser_Lamdba_Helper().send_png_data_to_slack(None, channel, 'AWS Billing', png_data)
        return png_data
    except Exception as error:
        message = f'Error in aws_web lambda: {error}'
        slack_message(message,[], channel)
        return message