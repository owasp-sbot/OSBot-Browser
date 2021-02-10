from gw_bot.api.Slack_Commands_Helper       import Slack_Commands_Helper
from osbot_aws.decorators.lambda_save_event import lambda_save_event
from osbot_aws.apis.shell.Lambda_Shell      import lambda_shell

# def cleanup_chrome_processes_and_tmp_files():               # remote temp files
#     for file in Files.find('/tmp/core.headless_shell.*'):
#         pid = file.split('.')[-1]
#         Process.run('pkill',['-TERM','-P',str(pid)])             # this doesn't seem to be working since the  "headless_shell <defunct>" is still there
#         Files.delete(file)



@lambda_shell
@lambda_save_event
def run(event, context):
    from osbot_browser.browser.Browser_Commands import Browser_Commands
    params  = event.get('params')
    data    = event.get('data' , {})
    channel = data.get('channel')

    result,_ = Slack_Commands_Helper(Browser_Commands).invoke(None, channel, params)

    #cleanup_chrome_processes_and_tmp_files()
    if channel is None:
        return result
    #return result