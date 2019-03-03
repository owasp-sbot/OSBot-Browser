import json

from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies


class DataTable_Js_Views:

    @staticmethod
    def _get_data(graph_name):
        from view_helpers.Vis_Js import Vis_Js
        vis_js = Vis_Js()
        return vis_js.get_graph_data(graph_name)

    @staticmethod
    def _create_table(headers,rows, team_id, channel,table_width='2000px', columns_defs=None, table_title=None):
        from view_helpers.DataTable_Js import DataTable_Js
        datatable_js              = DataTable_Js()
        datatable_js.table_width  = table_width
        datatable_js.columns_defs = columns_defs
        datatable_js.table_title  = table_title
        return datatable_js.create_table(headers, rows).send_screenshot_to_slack(team_id, channel)

    @staticmethod
    def graph(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);
        graph_name = params.pop(0)
        graph_data = DataTable_Js_Views._get_data(graph_name)

        if graph_data:
            nodes = graph_data.get('nodes')
            #headers = sorted(list(set(list(nodes.values()).pop())))
            #headers = [  'Issue Type', 'Summary', 'Description', 'Issue Links', 'Status' ,'Rating', 'Key']
            headers = ['Issue Type', 'Summary', 'Description', 'Status', 'Rating', 'Key'] # without issue links
            rows = []
            for index, node in enumerate(nodes.values()):
                row = [index + 1]
                for header in headers:
                    value = node.get(header)
                    if type(value).__name__ == 'dict':
                        value = json.dumps(value)
                    else:
                        value = Misc.remove_html_tags(value)
                    # if header == 'Issue Links':
                    #     value = "<span style='font-size: 8pt'>{0}</span>".format(value)
                    row.append(value)
                rows.append(row)
            headers.insert(0, '#')

            columns_defs = [
                {"targets": [1], "width": "100px"},     # Issue Type
                {"targets": [2], "width": "300px"},     # Summary
                #{"targets": [3], "width": "40%"}  ,     # Description
                #{"targets": [4], "width": "30%"}  ,     # Issue Links
            ]
            table_width = '1500px'
            return DataTable_Js_Views._create_table(headers, rows, team_id, channel,
                                                    table_width=table_width,
                                                    columns_defs = columns_defs,
                                                    table_title = "<b>{0}</b> <small><small><i>(data from graph)</i></small></small>".format(graph_name))

    @staticmethod
    def graph_all_fields(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);
        graph_data = DataTable_Js_Views._get_data(params.pop(0))

        if graph_data:
            nodes = graph_data.get('nodes')
            headers = sorted(list(set(list(nodes.values()).pop())))
            rows = []
            for index,node in enumerate(nodes.values()):
                row = [index+1]
                for header in headers:
                    value = node.get(header)
                    if type(value).__name__== 'dict':
                        value = json.dumps(value)
                    row.append(value)
                rows.append(row)
            headers.insert(0, '#')
            return DataTable_Js_Views._create_table(headers, rows, team_id, channel)

    def issue(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);


        graph_data = DataTable_Js_Views._get_data(params.pop(0))
        if graph_data:
            nodes   = graph_data.get('nodes')
            node    = list(nodes.values()).pop()
            fields = sorted(list(set(node)))
            rows = []
            for field in fields:
                row = ['<b>{0}</b>'.format(field)]
                value = node.get(field)
                if value:
                    if type(value).__name__ == 'dict':
                        value = json.dumps(value)
                    row.append(value)
                    rows.append(row)

            return DataTable_Js_Views._create_table(['name','value'], rows, team_id, channel)




    @staticmethod
    def test_data(team_id=None, channel=None, params=None):

        load_dependencies(['syncer', 'requests']);

        from view_helpers.DataTable_Js import DataTable_Js
        headers = ['Header AAA','Header BBB']
        rows    = [['value 1'  , 'value 2'  ],
                   ['value 3'  , 'value 4'  ],
                   ['value 5'               ],
                   [                        ],
                   ['value 6'  , 'value 7'  ],
                   [None                    ],
                   [None,'value 8', 'AB'    ],
                   ['value 9'  , 'value 10' ]]
        return DataTable_Js().create_table(headers, rows).send_screenshot_to_slack(team_id, channel)