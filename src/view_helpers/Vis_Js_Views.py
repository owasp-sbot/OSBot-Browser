from utils.aws.Lambdas import load_dependencies


class Vis_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']) ; from view_helpers.Vis_Js import Vis_Js

        graph_name = params.pop(0)
        vis_js = Vis_Js()
        vis_js.show_jira_graph(graph_name)
        return vis_js.send_screenshot_to_slack(team_id, channel)