from time import sleep

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
                nodes.append({'key': key, 'text': text , 'color': Misc.get_random_color()})

        for edge in graph_data.get('edges'):
            edges.append({ 'from': edge[0], 'text' : edge[1] ,'to': edge[2] ,'color':  Misc.get_random_color()})
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
        return go_js.render(nodes, edges, team_id=team_id, channel=channel)

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

        go_js.load_page(False)
        (nodes, edges) = Go_Js_Views._get_nodes_and_edges(graph_data,text_field='Summary')
        data = { "class": "go.TreeModel", "nodeDataArray": []}
        width  = Misc.to_int(Misc.array_pop(params, 0))
        height = Misc.to_int(Misc.array_pop(params, 0))
        if width and height:
            go_js.browser().sync__browser_width(width,height)
        else:
            go_js.set_browser_width_based_on_nodes(nodes)

        nodes_indexed = {}
        for index, node in enumerate(nodes):
            key  = node.get('key')
            text = node.get('text')
            nodes_indexed[key] = {'index':index, 'text': text }

        data['nodeDataArray'].append({"key": 0, "text": nodes[0].get('text')})                     # add root node first
        for edge in edges:
            parent    = nodes_indexed.get(edge['from']).get('index')
            key       = nodes_indexed.get(edge['to'  ]).get('index')
            text      = nodes_indexed.get(edge['to'  ]).get('text')
            item = {"key": key, "parent": parent, "text": text, "brush": Misc.get_random_color()}
            data['nodeDataArray'].append(item)

        go_js.invoke_js("create_graph_from_json", data)
        js_code = 'layoutAll()'
        go_js.api_browser.sync__await_for_element('#animationFinished')

        Dev.pprint(go_js.exec_js(js_code))
        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)

    @staticmethod
    def piechart(team_id=None, channel=None, params=None, headless=True):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "pie-chart", headless=headless)
        go_js.load_page(True)

        nodes =  [{ "key": 1,
                    "text": "Pie Chart from GSBot",
                    "slices": [{"start": -30 , "sweep": 60 , "color": "white"},
                               {"start": 30  , "sweep": 300, "color": "red"}]},
                  {  "key": 2,
                     "text": "partial circle",
                     "slices": [
                          { "start": 0  , "sweep": 120, "color": "lightgreen"},
                          { "start": 120, "sweep": 70 , "color": "blue"      },
                          { "start": 250, "sweep": 20 , "color": "yellow"    }]},
                  {  "key": 3, "text": "another circle"}]

        edges = [ {'from': 1, 'to': 2}, {'from': 2, 'to': 3} ]
        data = { 'edges': edges,'nodes': nodes}

        go_js.invoke_js('set_data', data)
        go_js.exec_js  ('init()')

        go_js.api_browser.sync__await_for_element('#animationFinished')

        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)

    @staticmethod
    def chart_js(team_id=None, channel=None, params=None, headless=True):

        def make_random_points(size=None, max=None):
            if size is None : size = 20
            if max is None  : max = 100
            return [Misc.random_number(0,max) for _ in range(0,size)]


        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "chart-js", headless=headless)
        go_js.load_page(True)

        #go_js.browser().sync__browser_width(1200)

        nodes = [{ "key": 1, "text": "Dynamically",                   "datasets": [{"label": "Random data"                                             ,"borderColor": "black", "data": make_random_points(8,10)}]},
                 { "key": 2, "text": "Created"    ,                   "datasets": [{"label": "First dataset"  ,"fill": False,"backgroundColor": "red"  ,"borderColor": "red"  , "data": make_random_points(8    )},
                                                                             {"label": "Second dataset" ,"fill": False,"backgroundColor": "blue" ,"borderColor": "blue" , "data": make_random_points(8    )}]},
                 { "key": 3, "text": "By GSBot"   , "color": "green", "datasets": [{"label": "some data"      ,"fill": False,"backgroundColor": "green","borderColor": "green", "data": make_random_points(     )}]}]
        edges = [{'from': 1, 'to': 2}, {'from': 1, 'to': 3}]
        data = {'edges': edges, 'nodes': nodes}

        go_js.invoke_js('create_graph',data)

        go_js.api_browser.sync__await_for_element('#animationFinished')
        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)


    def kanban(team_id=None, channel=None, params=None, headless=True):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "kanban",headless)
        go_js.load_page(True)

        go_js.browser().sync__browser_width(1000, 600)
        #(nodes, edges) = Go_Js_Views._get_nodes_and_edges(graph_data)
        #return go_js.render(nodes, edges, team_id=team_id, channel=channel)

        go_js.api_browser.sync__await_for_element('#animationFinished')
        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)