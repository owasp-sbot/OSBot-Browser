import json
from time import sleep

from osbot_aws.apis.Lambda import Lambda, load_dependencies

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc


class Go_Js_Views:

    @staticmethod
    def _get_graph_data(params,layout=None, headless=True):
        load_dependencies(['syncer', 'requests']);
        from osbot_browser.view_helpers.Go_Js import Go_Js

        graph_name = params.pop(0)

        go_js = Go_Js(headless=headless,layout=layout)
        graph_data = go_js.get_graph_data(graph_name)
        return go_js, graph_data

    @staticmethod
    def _get_nodes_and_edges(graph_data,nodes=None,edges=None, text_field='Key', append_key_to_text=False):
        if nodes is None: nodes = []
        if edges is None: edges = []
        if graph_data:
            for key,issue in graph_data.get('nodes').items():
                if issue and issue.get('Summary'):
                    text = issue.get(text_field)
                    if append_key_to_text:
                        text += " | {0}".format(key)
                else:
                    text = key
                nodes.append({'key': key, 'text': text, 'color': Misc.get_random_color()})

            for edge in graph_data.get('edges'):
                if edge[0] and edge[2]:
                    edges.append({ 'from': edge[0], 'text' : edge[1] ,'to': edge[2] ,'color':  Misc.get_random_color()})
                else:
                    print(edge)
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
    def mindmap_issue(team_id=None, channel=None, params=None):
        def log_message(message):
            slack_message(':point_right: {0}'.format(message),[],channel,team_id)

        def log_error(message):
            slack_message(':red_circle: {0}'.format(message),[],channel,team_id)

        (start, direction, depth, view) = (params.pop(0), 'all', 1, '')

        log_message('Step 1: Generating graph for issue {0} using direction `all` and depth `{1}`'.format(direction, depth))

        payload     = {"params": ['links', start, direction, depth, view]}
        result      = Lambda('gs.elastic_jira').invoke(payload)
        graph       = json.loads(result.get('text'))
        graph_name  = graph.get('graph_name')
        sleep(0.5)
        log_message('Step 2: Filtering graph {0} with filter `group_by_field` on field `Issue links`'.format(graph_name))
        payload = {"params": ["filter", "group_by_field", graph_name, "Issue Links"]}
        graph_filtered_name = Lambda('lambdas.gsbot.gsbot_graph').invoke(payload)
        if graph_name:
            log_message('Step 3: Creating  mindmap for filtered graph `{0}`'.format(graph_filtered_name))
            return Go_Js_Views.mindmap(team_id, channel, params=[graph_filtered_name], root_node_text=start)
        log_error('Error in step 2) No graph was created')


    @staticmethod
    def mindmap(team_id=None, channel=None, params=None, root_node_text=None):
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
        if len(nodes) > 0:
            for index, node in enumerate(nodes):
                key  = node.get('key')
                #text = "{1} | {0}".format(key,node.get('text'))                            # need a better way to trigger this
                text = node.get('text')
                nodes_indexed[key] = {'index':index, 'text': text }

            #root_node_text = "{1} | {0}".format(nodes[0].get('key'), nodes[0].get('text')) # and this
            if root_node_text is None:
                root_node_text = nodes[0].get('text')
            data['nodeDataArray'].append({"key": 0, "text": root_node_text })                     # add root node first
            for edge in edges:
                from_key   = edge['from']
                to_key     = edge['to']
                from_issue = nodes_indexed.get(from_key)
                to_issue   = nodes_indexed.get(to_key)

                if from_issue:
                    parent = nodes_indexed.get(edge['from']).get('index')
                else:
                    parent = from_key
                if to_issue:
                    key    = nodes_indexed.get(edge['to'  ]).get('index')
                    text   = nodes_indexed.get(edge['to'  ]).get('text')
                else:
                    key    = to_key
                    text   = to_key
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

        data = { "class": "go.GraphLinksModel",
                          "nodeDataArray": [{"key":"Problems"   , "text":"_Problems"    , "isGroup":True, "loc":"0 23.52284749830794" },
                                            {"key":"Reproduced" , "text":"_Reproduced"  , "isGroup":True, "color":"0", "loc":"109 23.52284749830794" },
                                            {"key":"Identified" , "text":"Identified"   , "isGroup":True, "color":"0", "loc":"235 23.52284749830794" },
                                            {"key":"Fixing"     , "text":"Fixing"       , "isGroup":True, "color":"0", "loc":"343 23.52284749830794" },
                                            {"key":"Reviewing"  , "text":"Reviewing"    , "isGroup":True, "color":"0", "loc":"451 23.52284749830794"},
                                            {"key":"Testing"    , "text":"Testing"      , "isGroup":True, "color":"0", "loc":"562 23.52284749830794" },
                                            {"key":"Customer"   , "text":"Customer"     , "isGroup":True, "color":"0", "loc":"671 23.52284749830794" },
                                            {"key":-1, "group":"Problems", "category":"newbutton",  "loc":"12 35.52284749830794" },
                                            {"key":1, "text":"text for oneA", "group":"Problems", "color":"0", "loc":"12 35.52284749830794"},
                                            {"key":2, "text":"text for oneB", "group":"Problems", "color":"1", "loc":"12 65.52284749830794"},
                                            {"key":3, "text":"text for oneC", "group":"Problems", "color":"0", "loc":"12 95.52284749830794"},
                                            {"key":4, "text":"text for oneD", "group":"Problems", "color":"1", "loc":"12 125.52284749830794"},
                                            {"key":5, "text":"text for twoA", "group":"Reproduced", "color":"1", "loc":"121 35.52284749830794"},
                                            {"key":6, "text":"text for twoB", "group":"Reproduced", "color":"1", "loc":"121 65.52284749830794"},
                                            {"key":7, "text":"text for twoC", "group":"Identified", "color":"0", "loc":"247 35.52284749830794"},
                                            {"key":8, "text":"text for twoD", "group":"Fixing", "color":"0", "loc":"355 35.52284749830794"},
                                            {"key":9, "text":"text for twoE", "group":"Reviewing", "color":"0", "loc":"463 35.52284749830794"},
                                            {"key":10, "text":"text for twoF", "group":"Reviewing", "color":"1", "loc":"463 65.52284749830794"},
                                            {"key":11, "text":"text for twoG", "group":"Testing", "color":"0", "loc":"574 35.52284749830794"},
                                            {"key":12, "text":"text for fourA", "group":"Customer", "color":"1", "loc":"683 35.52284749830794"},
                                            {"key":13, "text":"text for fourB", "group":"Customer", "color":"1", "loc":"683 65.52284749830794"},
                                            {"key":14, "text":"text for fourC", "group":"Customer", "color":"1", "loc":"683 95.52284749830794"},
                                            {"key":15, "text":"text for fourD", "group":"Customer", "color":"0", "loc":"683 125.52284749830794"},
                                            {"key":16, "text":"text for fiveA", "group":"Customer", "color":"0", "loc":"683 155.52284749830795"}
                                            ],
                          "linkDataArray": []}
                   # create_graph_from_json(data)
        go_js.invoke_js('create_graph_from_json',data)
        #go_js.api_browser.sync__await_for_element('#animationFinished')
        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)

    def timeline(team_id=None, channel=None, params=None, headless=True):
        (go_js, graph_data) = Go_Js_Views._get_graph_data(params, "timeline",headless)
        go_js.load_page(True)

        #go_js.browser().sync__browser_width(1000, 600)

        # var data = [
        #         { # this defines the actual time "Line" bar
        #           "key"         : "timeline", "category": "Line",
        #           "lineSpacing": 30,            # distance between timeline and event nodes
        #           "length"     : 700,           # the width of the timeline
        #           "start"      : datetime.now #new Date("1 Jan 2016"),
        #           "end: new Date("31 Dec 2016")
        #         },
        #
        #         # // the rest are just "events" --
        #         # // you can add as much information as you want on each and extend the
        #         # // default nodeTemplate to show as much information as you want
        #         # { event: "New Year's Day", date: new Date("1 Jan 2016") },
        #         # { event: "MLK Jr. Day", date: new Date("18 Jan 2016") },
        #         # { event: "Presidents Day", date: new Date("15 Feb 2016") },
        #         # { event: "Memorial Day", date: new Date("30 May 2016") },
        #         # { event: "Independence Day", date: new Date("4 Jul 2016") },
        #         # { event: "Labor Day", date: new Date("5 Sep 2016") },
        #         # { event: "Columbus Day", date: new Date("10 Oct 2016") },
        #         # { event: "Veterans Day", date: new Date("11 Nov 2016") },
        #         # { event: "Thanksgiving", date: new Date("24 Nov 2016") },
        #         # { event: "Christmas", date: new Date("25 Dec 2016") }
        #       ];
        #go_js.invoke_js('create_graph_from_json',data)


        #go_js.api_browser.sync__await_for_element('#animationFinished')
        return go_js.send_screenshot_to_slack(team_id=team_id, channel=channel)