from time import sleep

from osbot_aws.apis.Lambda import load_dependencies

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Edge_Format import Edge_Format
from osbot_browser.view_helpers.Node_Format import Node_Format


class VivaGraph_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False,headless=True):

        load_dependencies(['syncer', 'requests']);
        from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js

        graph_name = params.pop(0)
        vivagraph_js = VivaGraph_Js(headless=headless)  # will start browser

        graph_data = vivagraph_js.get_graph_data(graph_name)
        #
        vivagraph_js.load_page(False)
        if graph_data:
            edges = graph_data.get('edges')
            nodes = []
            for key,issue in graph_data.get('nodes').items():
                if issue and issue.get("Image Url") :
                    (label, img_size, img_url) = (key,20,issue.get("Image Url"))
                else:
                    (label,img_size,img_url) = vivagraph_js.resolve_icon_from_issue_type(issue, key)
                node = {
                            'key'        : key     ,
                            'label'      : label   ,
                            'img_url'    : img_url ,
                            'img_size'   : img_size,
                            #'issue_type' : issue.get('Issue Type'),
                            #'summary'    : issue.get('Summary')
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


    # def people(team_id=None, channel=None, params=None, no_render=False,headless=True):
    #
    #     (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params,no_render=True,headless=headless)
    #
    #
    #     return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, {}, team_id, channel)