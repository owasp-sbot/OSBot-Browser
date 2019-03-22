from time import sleep

from utils.Dev import Dev
from utils.Lambdas_Helpers import slack_message
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies
from view_helpers.Edge_Format import Edge_Format
from view_helpers.Node_Format import Node_Format


class VivaGraph_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False,headless=True):

        load_dependencies(['syncer', 'requests']);
        from view_helpers.VivaGraph_Js import VivaGraph_Js

        graph_name = params.pop(0)
        vivagraph_js = VivaGraph_Js(headless=headless)  # will start browser

        graph_data = vivagraph_js.get_graph_data(graph_name)
        #
        vivagraph_js.load_page(False)
        if graph_data:
            edges = graph_data.get('edges')
            nodes = []
            for key,issue in graph_data.get('nodes').items():
                (label,img_size,img_url) = vivagraph_js.resolve_icon_from_issue_type(issue, key)
                node = {
                            'key'     : key     ,
                            'label'   : label   ,
                            'img_url' : img_url ,
                            'img_size': img_size
                        }
                nodes.append(node)
            slack_message(":point_right: Rendering `{0}` using VivaGraph JS engine (`{1}` nodes and `{2}` edges)"
                          .format(graph_name, len(nodes), len(edges)), [], channel,team_id)



            if no_render is True:
                return graph_name, nodes, edges, graph_data, vivagraph_js

            options = {}
            return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, options, team_id, channel)



    @staticmethod
    def by_issue_type(team_id=None, channel=None, params=None):
        params.append('Issue Type')
        return VivaGraph_Js_Views.by_field(team_id, channel, params)

    @staticmethod
    def by_rating(team_id=None, channel=None, params=None):
        params.append('Rating')
        return VivaGraph_Js_Views.by_field(team_id, channel, params)

    @staticmethod
    def by_field(team_id=None, channel=None, params=None):

        if len(params) < 2:
            text = ':red_circle: Hi, for the `by_field` command, you need to provide a field name, for example: `Summary`, `Issue Type`,`Rating`, `Status`  '
            return text

        (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params,no_render=True)
        field = ' '.join(params)
        for node in nodes:
            key   = node.get('key')
            issue = graph_data.get('nodes').get(key)
            if issue:
                value = issue.get(field)
                node['label'] = value

        return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, {}, team_id, channel)


    def people(team_id=None, channel=None, params=None, no_render=False,headless=True):

        (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params,no_render=True,headless=headless)
        from utils.slack.API_Slack import API_Slack
        slack = API_Slack(team_id='T0SDK1RA8')
        Dev.pprint(slack.user('U4AF226H0'))
        # users = self.api.users()
        for node in nodes:
            if node.get('key') == 'GSP-95':
                node['img_url'] = 'https://ca.slack-edge.com/T0SDK1RA8-U4AF226H0-4606985f1305-72'

                return

        #Dev.pprint(len(set(users)))

        return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, {}, team_id, channel)