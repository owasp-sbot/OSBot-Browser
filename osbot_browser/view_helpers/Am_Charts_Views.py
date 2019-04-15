from time import sleep

from osbot_aws.apis.Lambda import load_dependencies

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc


class Am_Charts_Views:

    @staticmethod
    def _get_graph_data(params,layout=None, headless=True):
        load_dependencies(['syncer', 'requests']);
        from osbot_browser.view_helpers.Am_Charts import Am_Charts

        am_charts  = Am_Charts(headless=headless,layout=layout)
        graph_name = Misc.array_pop(params,0)
        if graph_name:
            graph_data = am_charts.get_graph_data(graph_name)
            return am_charts, graph_data
        return am_charts,None


    @staticmethod
    def default(team_id=None, channel=None, params=None,headless=True):
        (am_charts, graph_data) = Am_Charts_Views._get_graph_data(params,headless=headless)
        (nodes,edges)           = am_charts.get_nodes_and_edges(graph_data)

        return am_charts.render(nodes, edges,team_id = team_id, channel= channel )

    @staticmethod
    def triangle(team_id=None, channel=None, params=None, headless=True):
        (am_charts, graph_data) = Am_Charts_Views._get_graph_data(params, headless=headless)
        am_charts.load_page(True)

        js_code = """
var chart = am4core.create("chartdiv", am4charts.SlicedChart);


var series = chart.series.push(new am4charts.PyramidSeries());
series.colors.step = 2;
series.dataFields.value = "value";
series.dataFields.category = "name";
series.alignLabels = true;
series.labelsContainer.width = 200;
series.labelsContainer.paddingLeft = 15;

chart.legend = new am4charts.Legend();
chart.legend.padding(20,20,20,20);

chart.___data = "" 
        """
        data = [{ "name": "High"    , "value": 100},
                 {"name": "Moderate", "value": 100},
                 {"name": "Low"     , "value": 100},
                 ]
        am_charts.exec_js(js_code)
        am_charts.assign_variable_js('window.chart.data',data)

        return am_charts.send_screenshot_to_slack(team_id, channel)

    @staticmethod
    def chord(team_id=None, channel=None, params=None, headless=True):
        load_dependencies(['syncer', 'requests']);
        from osbot_browser.view_helpers.Am_Charts import Am_Charts
        (am_charts, graph_data) = Am_Charts_Views._get_graph_data(params, headless=headless)

        am_charts.load_page(True)
        js_code= """
var chart = am4core.create("chartdiv", am4charts.ChordDiagram);
chart.hiddenState.properties.opacity = 0;

chart.dataFields.fromName = "from";
chart.dataFields.toName = "to";
chart.dataFields.value = "value";

// make nodes draggable
var nodeTemplate = chart.nodes.template;
nodeTemplate.readerTitle = "Click to show/hide or drag to rearrange";
nodeTemplate.showSystemTooltip = true;
nodeTemplate.cursorOverStyle = am4core.MouseCursorStyle.pointer
"""
        am_charts.exec_js(js_code)

        data = [{ "from": "A", "to": "D", "value": 1 },
                { "from": "B", "to": "D", "value": 1 },
                { "from": "B", "to": "E", "value": 1 },
                { "from": "B", "to": "C", "value": 1 },
                { "from": "C", "to": "E", "value": 1 },
                { "from": "E", "to": "D", "value": 1 },
                { "from": "C", "to": "A", "value": 1 },
                { "from": "G", "to": "A", "value": 1 },
                { "from": "D", "to": "B", "value": 1 }];


        data = []
        for edge in graph_data.get('edges'):
            data.append({ "from": edge[0], "to": edge[2], "value": 1 })

        am_charts.assign_variable_js('window.chart.data',data)

        return am_charts.send_screenshot_to_slack(team_id, channel)