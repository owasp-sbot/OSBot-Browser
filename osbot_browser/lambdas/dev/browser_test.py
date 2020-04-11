from osbot_aws.Dependencies            import load_dependencies
from osbot_aws.apis.shell.Shell_Server import lambda_shell
from osbot_utils.utils.Process         import Process


# class Lambda_Shell:
#
#     def run_command(self,shell_command):
#         if shell_command:
#             executable = shell_command.get('executable')
#             params     = shell_command.get('params')
#             cwd        = shell_command.get('cwd')
#             return Process.run(executable, params=params, cwd=cwd)


@lambda_shell
def run(event, context=None):

    #shell_command = event.get('shell_command')
    #if shell_command:
    #    return Lambda_Shell().run_command(shell_command)

    return 'here'
    code = event.get('code')
    if code:
        return exec(code)


    load_dependencies('syncer,requests,pyppeteer,websocket-client')

    url = event.get('url')
    #from osbot_browser.browser.Browser_Page import Browser_Page
    #page = Browser_Page().setup()

    #page.open(url)
    #return page.screenshot()
    # return page.text()
    # return page.url(), page.text()

    from osbot_browser.browser.API_Browser import API_Browser

    api_browser = API_Browser().sync__setup_browser().set_auto_close(False)

    if url:
        api_browser.sync__open(url)

    return api_browser.sync__screenshot_base64()
    #return api_browser.sync__url()
