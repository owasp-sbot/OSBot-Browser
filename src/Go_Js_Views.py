from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies


class Go_Js_Views:

    @staticmethod
    def _get_graph_data(params,layout=None, headless=True):
        load_dependencies(['syncer', 'requests']);
        from view_helpers.Go_Js import Go_Js

        graph_name = params.pop(0)

        go_js = Go_Js(headless=headless,layout=layout)
        graph_data = go_js.get_graph_data(graph_name)
        return go_js, graph_data

    @staticmethod
    def _get_nodes_and_edges(graph_data,nodes=None,edges=None, text_field='Key', append_key_to_text=False):
        if nodes is None: nodes = []
        if edges is None: edges = []

        for key,issue in graph_data.get('nodes').items():
            if issue and issue.get('Summary'):
                text = issue.get(text_field)
                if append_key_to_text:
                    text += " | {0}".format(key)
                nodes.append({'key': key, 'text': text})

        for edge in graph_data.get('edges'):
            edges.append({ 'from': edge[0], 'text' : edge[1] ,'to': edge[2] ,'color': 'blue'})
        return nodes,edges

    @staticmethod
    def default(team_id=None, channel=None, params=None):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params)
        (nodes,edges)       = Go_Js_Views._get_nodes_and_edges(graph_data)

        return go_js.render(nodes, edges, width=2000,team_id = team_id, channel= channel )

    @staticmethod
    def circular(team_id=None, channel=None, params=None):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params,"circular")
        (nodes, edges) = Go_Js_Views._get_nodes_and_edges(graph_data, text_field='Summary', append_key_to_text=True)
        return go_js.render(nodes, edges, width=3000, team_id=team_id, channel=channel)

    @staticmethod
    def sankey(team_id=None, channel=None, params=None):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "sankey")
        (nodes, edges) = Go_Js_Views._get_nodes_and_edges(graph_data)
        return go_js.render(nodes, edges, width=2000, team_id=team_id, channel=channel)

    @staticmethod
    def swimlanes(team_id=None, channel=None, params=None):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "swimlanes")


        nodes = [{'key': "Pool1", 'text': "By Risk",  'isGroup': True, 'category': "Pool"}]
        edges = []
        groups = []
        colors = ["lightblue","lightgreen","lightyellow","orange"]
        for key,issue in graph_data.get('nodes').items():
            if issue:
                group = Misc.array_add(groups, issue.get('Rating'))
                nodes.append({'key': key, 'group':group}) #issue.get('Summary')
        for group in list(set(groups)):
            nodes.append({'key': group, 'text': group, 'isGroup': True, 'group'   : "Pool1", 'color': Misc.array_pop(colors)})

        for edge in graph_data.get('edges'):
            edges.append({ 'from': edge[0],'to': edge[2]})

        js_code = 'relayoutLanes()'
        return go_js.render(nodes, edges, js_code=js_code, width=1400, team_id=team_id, channel=channel)

    @staticmethod
    def mindmap(team_id=None, channel=None, params=None):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "mindmap",headless=True)

        go_js.load_page(True)
        go_js.browser().sync__browser_width(300)
        data = {
            "class": "go.TreeModel",
            "nodeDataArray": [
                {"key": 0, "text": "Mind Map"},
                {"key": 1, "parent": 0, "text": "Getting more time", "brush": "skyblue"},
                {"key": 2, "parent": 0, "text": "1cGetting 1234....AAAA", "brush": "skyblue"},
                {"key": 3, "parent": 0, "text": "2cGetting 4567....", "brush": "skyblue"}]
        }
        #

        #
        # for index, node in enumerate(nodes):
        #     key = node.get('key')
        #     item = {"key": index, "parent": 0, "text":key, "brush": "skyblue"}
        #     data['nodeDataArray'].append(item)

        (nodes, edges) = Go_Js_Views._get_nodes_and_edges(graph_data)
        #data = { "class": "go.TreeModel", "nodeDataArray": []}
        for index, node in enumerate(nodes):
            key = node.get('key')
            print(key)

        go_js.invoke_js("create_graph_from_json", data)
        go_js.api_browser.sync__await_for_element('#animationFinished')
        from time import sleep
        #sleep(1)
        return go_js.send_screenshot_to_slack()
        #return go_js.render(nodes, edges, width=400, team_id=team_id, channel=channel)

