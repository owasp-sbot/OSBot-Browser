from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.Dependencies import load_dependencies
from osbot_utils.utils import Misc
from osbot_utils.utils.Misc import to_int


class VivaGraph_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, screenshot=True,no_render=False,headless=True):
        load_dependencies('syncer,requests,pyppeteer');
        from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js

        graph_name = params[0]

        vivagraph_js = VivaGraph_Js(headless=headless)

        if len(params) > 1:
            vivagraph_js.browser_width = to_int(params[1], None)
        if len(params) > 2:
            vivagraph_js.render_wait = to_int(params[2], None)

        graph_data = vivagraph_js.get_graph_data(graph_name)

        if graph_data:

            (nodes,edges) = vivagraph_js.get_nodes_edges_from_graph_data(graph_data)

            if no_render is True:
                return graph_name, nodes, edges, graph_data, vivagraph_js


            return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, graph_name, screenshot, team_id, channel)
            # else:
            #     vivagraph_js.create_graph(nodes, edges)
            # options = {}

    @staticmethod
    def no_key(team_id=None, channel=None, params=None, headless=True,screenshot=True):

        (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params, no_render=True, headless=headless)
        issues = graph_data.get('nodes')
        for node in nodes:
            key = node.get('key')
            if issues.get(key):             # if it is an Issue Id, remove the keys (if not Leave it there)
                node['label'] = ''

        return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, graph_name, screenshot, team_id, channel)

    @staticmethod
    def node_value(team_id=None, channel=None, params=None,headless=True,screenshot=True):

        if len(params) < 2:
            text = ':red_circle: Hi, for the `node_value` command, you need to provide a field name, for example: `Summary`, `Issue_Type`,`Rating`, `Status`  '
            return text

        field = params[1].replace('_', ' ')   #  Add support for fields with a space
        del params[1]                         #  We need to remove it so that it doesn't affect the other params like width or delay.
        (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params,no_render=True,headless=headless)

        for node in nodes:
            key   = node.get('key')
            issue = graph_data.get('nodes').get(key)
            if issue:
                value = issue.get(field)
                node['label'] = value

        return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, graph_name, screenshot, team_id, channel)


    # def people(team_id=None, channel=None, params=None, no_render=False,headless=True):
    #
    #     (graph_name, nodes, edges, graph_data, vivagraph_js) = VivaGraph_Js_Views.default(team_id, channel, params,no_render=True,headless=headless)
    #
    #
    #     return vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges, {}, team_id, channel)