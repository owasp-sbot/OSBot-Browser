from osbot_aws.apis.Lambda import load_dependencies

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Edge_Format import Edge_Format
from osbot_browser.view_helpers.Node_Format import Node_Format


class Vis_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False, headless=True):

        load_dependencies(['syncer', 'requests']) ; from osbot_browser.view_helpers.Vis_Js import Vis_Js

        graph_name = params.pop(0)
        vis_js = Vis_Js(headless=headless)                               # will start browser
        graph_data = vis_js.get_graph_data(graph_name)

        nodes = []
        edges = []
        vis_js.load_page(False)
        if graph_data:
            graph_name = graph_data.get('graph_name')
            for key, issue in graph_data.get('nodes').items():
                nodes.append({'id': key, 'label': key})
                # Dev.pprint(issue)

            for edge in graph_data.get('edges'):
                from_node = edge[0]
                link_type = edge[1]
                to_node = edge[2]
                edges.append({'from': from_node, 'to': to_node, 'label': link_type})

            if no_render is False:
                vis_js.create_graph(nodes, edges, {}, graph_name)

        if no_render is True:
            return (graph_name,nodes, edges, graph_data,vis_js)

        return vis_js.send_screenshot_to_slack(team_id, channel)

    @staticmethod
    def no_labels(team_id=None, channel=None, params=None):

        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)
        graph_name += ' | no_labels'

        for node in nodes:
            del node['label']

        for edge in edges:
            del edge['label']

        return vis_js.create_graph_and_send_screenshot_to_slack(graph_name, nodes,edges, None, team_id, channel)

    @staticmethod
    def node_label(team_id=None, channel=None, params=None):
        if len(params) < 2:
            return "':red_circle: Hi, for the `node_label` view, you need to provide the label field name. Try: `Key`, `Summary`, `Rating`, `Status`"

        label_key  = ' '.join(params[1:])

        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)
        graph_name += ' | node_label | ' + label_key

        issues = graph_data.get('nodes')
        for node in nodes:
            issue = issues.get(node['label'])
            if issue:
                value = str(issue.get(label_key))
                node['label'] = Misc.word_wrap(value,40)

        for edge in edges:
            del edge['label']

        options = { 'nodes': {'shape' : 'box' },
                    'edges': {'arrows': 'to'  }}
        options = None
        return vis_js.create_graph_and_send_screenshot_to_slack(graph_name, nodes,edges, options, team_id, channel)

    # Issues layouts

    @staticmethod
    def by_rating(team_id=None, channel=None, params=None):
        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)
        graph_name += ' | by_rating'
        issues = graph_data.get('nodes')
        options ={}
        for node in nodes:
            issue = issues.get(node.get('id'))
            (
                    Node_Format .rating_color(node, issue)
                                .size_by_r123(node, issue)
                                #.set_Label   (node, issue, 'Summary')
                                #.only_highs  (node, issue)
                                #.add_Key_to_Label(node)
            )

        for edge in edges:
            edge['label'] = ''

        return (    vis_js.load_page(True)
                          .create_graph(nodes, edges, options, graph_name)
                          .browser_width(3000)
                          .send_screenshot_to_slack(team_id, channel) )

    def by_status(team_id=None, channel=None, params=None):
        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)
        graph_name += ' | by_status'
        issues = graph_data.get('nodes')

        for node in nodes:
            issue = issues.get(node.get('id'))
            (
                    Node_Format .status_color    (node, issue)
                                .size_by_r123    (node, issue, False)
                                .set_label       (node, issue, 'Summary')
                                #.only_highs     (node, issue)
                                .add_key_to_label(node)
                                .add_status_to_label(node, issue)
                                #.no_label       (node)
                                #.set_r1_positions(node)
            )

        for edge in edges:
            edge['label'] = ''

        #edges = []
        options = {}
        return (    vis_js.load_page(True)
                          .create_graph(nodes, edges, options, graph_name)
                          .browser_width(2000)
                          .send_screenshot_to_slack(team_id, channel) )

    @staticmethod
    def by_issue_type(team_id=None, channel=None, params=None, headless=True):
        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True,headless=headless)
        graph_name += ' | by_issue_type'

        issues = graph_data.get('nodes')
        options = {}
        for node in list(nodes):
            issue_id = node.get('id')

            #if issue_id =='GSSP-115': nodes.remove(node)

            issue = issues.get(issue_id)
            (
                Node_Format .issue_type_color       (node, issue, True)
                            .size_by_r123           (node, issue, False)
                            .set_label              (node, issue, 'Summary')
                            .add_issue_type_to_label(node, issue)
                            #.no_label        (node)
                            #.add_Key_to_Label (node)
            )

        Edge_Format.no_labels(edges)

        return (vis_js.load_page(True)
                .create_graph(nodes, edges, options, graph_name)
                .browser_width(2000)
                .send_screenshot_to_slack(team_id, channel))

    @staticmethod
    def r1_pinned(team_id=None, channel=None, params=None,headless=False):
        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True,headless=headless)
        graph_name += ' | r1_pinned'

        issues = graph_data.get('nodes')
        Edge_Format.removed_non_risk_edge_sinks(edges,nodes)

        options = {}
        for node in list(nodes):
            issue_id = node.get('id')

            #if issue_id =='GSSP-115': nodes.remove(node)

            issue = issues.get(issue_id)
            (
                Node_Format .issue_type_color       (node, issue, True)
                            .size_by_r123           (node, issue, False)
                            .set_label              (node, issue, 'Summary')
                            .add_issue_type_to_label(node, issue)
                            .no_label_for_issue_type(node, issue,'Vulnerability')
                            #.no_label        (node)
                            .add_key_to_label (node)
            )

        Node_Format.remove_fixed_and_fp(nodes,issues)

        Edge_Format.no_labels(edges)

        return (vis_js.load_page(True)
                .create_graph(nodes, edges, options, graph_name)
                .browser_width(2500)
                .set_fixed_r1_nodes()
                .wait_n_seconds(3)
                .send_screenshot_to_slack(team_id, channel))

    @staticmethod
    def r1_r4(team_id=None, channel=None, params=None):

        options = {
            'nodes': { 'shape' : 'box'},
            'edges': { 'arrows': 'to' },
            'physics': {
                'barnesHut': {
                    'avoidOverlap': 0.1
                },
            }}

        (graph_name,nodes, edges, graph_data,vis_js) = Vis_Js_Views.default(params=params, no_render=True)

        def format_node(node):
            issue = graph_data.get('nodes').get(node.get('id'))
            if issue:
                node['label'] = Misc.word_wrap(issue.get('Summary'),20)
                #node['label'] = issue.get('Rating')
                labels = issue.get('Labels')
                if 'R0' in labels:
                    #node['label'] = issue.get('Summary')
                    node['color'] = '#FF0000'
                    node['font' ] = {'color' : 'white', 'size': 25 }
                    node['mass' ] = 2
                    return node

                if 'R1' in labels:
                    node['color'] = '#FF6666'
                    node['font'] = {'size': 20}
                    node['mass'] = 3
                    return node

                if 'R2' in labels:
                    node['color'] = '#FFAAAA'
                    node['font'] = {'size': 15}
                    #node['mass'] = 1
                    return node

                if 'R3' in labels:
                    node['color'] = '#FFDDDD'

                    return node

                if 'R4' in labels:
                    node['color'] = '#00DDDD'

                    return node
                #Dev.pprint(issue)

        fixed_nodes = []
        for node in nodes:
            fixed_node = format_node(node)
            if fixed_node:
                Node_Format.add_key_to_label(fixed_node)
                fixed_nodes.append(fixed_node)

        for edge in edges:
            edge['label'] =''

        #edges = []
        vis_js.load_page(True)
        vis_js.create_graph(fixed_nodes, edges, options,graph_name)
        vis_js.browser().sync__browser_width(2000)
        return vis_js.send_screenshot_to_slack(team_id, channel)
        #return vis_js.create_graph_and_send_screenshot_to_slack(fixed_nodes, edges, options, team_id, channel)
