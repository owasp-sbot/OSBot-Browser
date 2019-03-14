from utils.Dev import Dev
from utils.Lambdas_Helpers import slack_message
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies
from view_helpers.Edge_Format import Edge_Format
from view_helpers.Node_Format import Node_Format


class VivaGraph_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False):

        load_dependencies(['syncer', 'requests']);
        from view_helpers.VivaGraph_Js import VivaGraph_Js

        graph_name = params.pop(0)
        vivagraph_js = VivaGraph_Js(headless=False)  # will start browser

        graph_data = vivagraph_js.get_graph_data(graph_name)
        #
        vivagraph_js.load_page(False)
        if graph_data:
            nodes = graph_data.get('nodes')
            edges = graph_data.get('edges')
            slack_message(":point_right: rendering graph {0} using VivaGraph JS engine, with {1} nodes and {2} edges"
                          .format(graph_name, len(nodes), len(edges)), [], channel,team_id)
            # graph_name = graph_data.get('graph_name')
            # for key, issue in graph_data.get('nodes').items():
            #     nodes.append({'id': key, 'label': key})
            #     # Dev.pprint(issue)
            #
            # for edge in graph_data.get('edges'):
            #     from_node = edge[0]
            #     link_type = edge[1]
            #     to_node = edge[2]
            #     edges.append({'from': from_node, 'to': to_node, 'label': link_type})

            if no_render is False:
                vivagraph_js.create_graph(nodes, edges, graph_data, graph_name)
        if 100 < len(nodes) < 200:
            vivagraph_js.browser().sync__browser_width(2000)
        if len(nodes) > 200:
            vivagraph_js.browser().sync__browser_width(3000)
        if no_render is True:
            return (graph_name, nodes, edges, graph_data, vivagraph_js)
        from time import sleep
        sleep(5)
        return vivagraph_js.send_screenshot_to_slack(team_id, channel)