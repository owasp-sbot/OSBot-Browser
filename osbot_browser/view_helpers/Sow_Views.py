from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Sow(Base_View_Helpers):
    def __init__(self,headless=True, layout=None):
        if layout:
            self.web_page = '/sow/{0}.html'.format(layout)
        else:
            self.web_page = '/sow/simple.html'

        super().__init__(web_page=self.web_page,headless=headless)

class Sow_Views:
    current_version = "v0.20"

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False, headless=True):

        maps = Sow(headless)
        maps.load_page(True)

        issue_data = {
            "requirement_number"   : "1A - Determine File Type"                                 ,
            "requirement_language" : "N/A"                                                      ,
            "verification_method"  : "Test"                                                     ,
            "setup"                : ""                                                         ,
            "execution_steps"      : "<ol><li></li><li></li><li></li><li></li><li></li></ol>"   ,
            "expected_result"      : ''                                                         ,
            "compliance"           : '&lt;Compliant | Partially Compliant | Non-Compliant &gt;' ,
            "results"              : "{0}".format(params)
        }
        maps.invoke_js('set_data', issue_data)
        return maps.send_screenshot_to_slack('not-used', channel)

    @staticmethod
    def view(team_id=None, channel=None, params=None):

        if params and len(params) ==1:
            issue_id = params.pop()
            from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
            from osbot_aws.apis.Lambda import Lambda

            lambda_name = 'osbot_browser.lambdas.gw.sow'

            png_data    = Lambda(lambda_name).invoke({'issue_id': issue_id})
            if png_data is None:
                return f':red_circle: No png data created for {issue_id}'
            if channel is None:
                return png_data
            else:
                title = f'howing issue: {issue_id}'
                Browser_Lamdba_Helper().send_png_data_to_slack(team_id, channel, title, png_data)
        else:
            return f":red_circle: Missing `jira_id` param, try SOW-121"

