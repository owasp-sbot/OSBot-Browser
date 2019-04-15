import json

from osbot_aws.apis.Lambda import load_dependencies

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc


class DataTable_Js_Views:

    @staticmethod
    def _get_data(graph_name):
        from osbot_browser.view_helpers.Vis_Js import Vis_Js
        vis_js = Vis_Js()
        return vis_js.get_graph_data(graph_name)

    @staticmethod
    def _create_table(headers,rows, team_id, channel,table_width='1200px', columns_defs=None, table_title=None):
        from osbot_browser.view_helpers.DataTable_Js import DataTable_Js
        datatable_js              = DataTable_Js()
        datatable_js.table_width  = table_width
        datatable_js.columns_defs = columns_defs
        datatable_js.table_title  = table_title
        return datatable_js.create_table(headers, rows).send_screenshot_to_slack(team_id, channel)

    @staticmethod
    def _create_table_with_headers(team_id, channel, graph_name, headers, columns_defs=[], table_width='1200px'):
        graph_data = DataTable_Js_Views._get_data(graph_name)
        if graph_data:
            nodes = graph_data.get('nodes')
            rows = []
            for index, node in enumerate(nodes.values()):
                row = [index + 1]
                for header in headers:
                    value = node.get(header)
                    if type(value).__name__ == 'dict':
                        value = json.dumps(value)
                    else:
                        value = Misc.remove_html_tags(value)
                    row.append(value)
                rows.append(row)
            headers.insert(0, '#')

            return DataTable_Js_Views._create_table(headers, rows, team_id, channel,
                                                    table_width  = table_width,
                                                    columns_defs = columns_defs,
                                                    table_title  = "<b>{0}</b> <small><small><i>(data from graph)</i></small></small>".format(graph_name))
    @staticmethod
    def graph(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);
        graph_name = params.pop(0)
        headers      = ['Issue Type', 'Summary', 'Description', 'Status', 'Rating', 'Key']  # without issue links
        table_width  = "1500px"
        columns_defs = [
            {"targets": [1], "width": "60px"},  # Key
            {"targets": [2], "width": "600px"},  # Summary
        ]
        return DataTable_Js_Views._create_table_with_headers(team_id, channel, graph_name,headers, columns_defs, table_width)

    @staticmethod
    def graph_simple(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);
        graph_name = params.pop(0)
        table_width = "1200px"
        headers     = ['Key', 'Summary', 'Status', 'Rating', 'Issue Type']  # without issue links
        columns_defs = [
            {"targets": [1], "width": "60px"},  # Key
            #{"targets": [1], "width": "600px"},  # Summary
            {"targets": [3], "width": "150px"},  # Status
            {"targets": [5], "width": "150px"},  # Status
        ]

        return DataTable_Js_Views._create_table_with_headers(team_id, channel, graph_name, headers, columns_defs,table_width)

    @staticmethod
    def graph_tasks(team_id=None, channel=None, params=None):
        load_dependencies(['syncer', 'requests']);
        graph_name = params.pop(0)
        table_width = "1200px"
        headers = ['Key', 'Summary', 'Latest_Information','Status', 'Issue Type']  # without issue links
        columns_defs = [
            {"targets": [1], "width": "70px"},  # Key
            {"targets": [1], "width": "300px"},  # Summary
            {"targets": [2], "width": "300px"},  # Latest_Information
            #{"targets": [3], "width": "100px"},  # Status
            #{"targets": [5], "width": "100px"},  # Rating
        ]

        return DataTable_Js_Views._create_table_with_headers(team_id, channel, graph_name, headers, columns_defs,
                                                             table_width)

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

        from osbot_browser.view_helpers.DataTable_Js import DataTable_Js
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