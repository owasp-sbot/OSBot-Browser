from utils.Dev import Dev
from utils.aws.Lambdas import load_dependencies


class Go_Js_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None, no_render=False):
        load_dependencies(['syncer', 'requests']);
        from view_helpers.Go_Js import Go_Js

        graph_name = params.pop(0)

        go_js = Go_Js(headless=False)  # will start browser

        #graph_data = go_js.get_graph_data(graph_name)
        #Dev.pprint(len(graph_data))

        nodes = [ { 'key': "Alpha" , 'color': "lightblue" },
                  { 'key': "Beta"  , 'color': "orange"    },
                  { 'key': "Gamma" , 'color': "lightgreen"},
                  { 'key': "Delta" , 'color': "pink"      },

                  ]
        edges = [ { 'from': "Alpha", 'to': "Beta" },
                  { 'from': "Alpha", 'to': "Gamma" },
                  { 'from': "Beta"    , 'to': "Beta" },
                  { 'from': "Gamma", 'to': "Delta" },
                  { 'from': "Delta", 'to': "Alpha" }
                ]

        go_js.create_graph_and_send_screenshot_to_slack(nodes,edges,None, team_id, channel)


