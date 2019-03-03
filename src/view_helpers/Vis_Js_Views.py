from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies


class Vis_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False):

        load_dependencies(['syncer', 'requests']) ; from view_helpers.Vis_Js import Vis_Js

        graph_name = params.pop(0)
        vis_js = Vis_Js()
        graph_data = vis_js.get_graph_data(graph_name)
        nodes = []
        edges = []
        vis_js.load_page(False)
        if graph_data:
            for key, issue in graph_data.get('nodes').items():
                nodes.append({'id': key, 'label': key})
                # Dev.pprint(issue)

            for edge in graph_data.get('edges'):
                from_node = edge[0]
                link_type = edge[1]
                to_node = edge[2]
                edges.append({'from': from_node, 'to': to_node, 'label': link_type})

            if no_render is False:
                vis_js.create_graph(nodes, edges)

        if no_render is True:
            return (nodes, edges, graph_data,vis_js)

        return vis_js.send_screenshot_to_slack(team_id, channel)

    @staticmethod
    def no_labels(team_id=None, channel=None, params=None):

        (nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)

        for node in nodes:
            del node['label']

        for edge in edges:
            del edge['label']

        return vis_js.create_graph_and_send_screenshot_to_slack(nodes,edges, None, team_id, channel)

    @staticmethod
    def node_label(team_id=None, channel=None, params=None):

        if len(params) != 2:
            return "':red_circle: Hi, for the `node_label` view, you need to provide the label field name. Try: `Key`, `Summary`, `Rating`, `Status`"

        #graph_name = params[0]
        label_key  = params[1]
        (nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)

        issues = graph_data.get('nodes')
        for node in nodes:
            issue = issues.get(node['label'])
            if issue:
                value = str(issue.get(label_key))
                node['label'] = Misc.word_wrap(value,40)

        for edge in edges:
            del edge['label']

        options = { 'nodes': {'shape' : 'box'} }

        return vis_js.create_graph_and_send_screenshot_to_slack(nodes,edges, options, team_id, channel)
