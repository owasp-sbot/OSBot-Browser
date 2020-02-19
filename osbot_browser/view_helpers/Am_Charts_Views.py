import json
from time import sleep

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_aws.Dependencies import load_dependencies


class Am_Charts_Views:

    @staticmethod
    def _get_graph_data(params,layout=None, headless=True):
        load_dependencies('syncer,requests,pyppeteer');
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
    def chord(team_id=None, channel=None, params=None, headless=True):
        load_dependencies('syncer,requests,pyppeteer');
        (am_charts, graph_data) = Am_Charts_Views._get_graph_data(params, headless=headless)
        Dev.pprint(graph_data)
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


    #todo: rewrite this to make it only usable from Jupyter (for this to work from slack, we need to get the timeline from a graph)
    @staticmethod
    def timeline(team_id=None, channel=None, params=None, headless=True):
        load_dependencies('syncer,requests,pyppeteer');
        from osbot_browser.view_helpers.Am_Charts import Am_Charts

        am_charts = Am_Charts(headless=headless)
        Misc.array_pop(params,0)        # remove the graph name (which is not used)
        width  = Misc.to_int(Misc.array_pop(params, 0))
        height = Misc.to_int(Misc.array_pop(params, 0))
        clip = {'x': 0, 'y': 50, 'width': width, 'height': height-100}
        #clip  = None

        am_charts.browser().sync__browser_width(width, height)
        try:
            data = json.loads(" ".join(params))
            am_charts.load_page(True)

            js_code = """
// Create chart instance
var chart = am4core.create("chartdiv", am4charts.XYChart);

// Create axes
var xAxis = chart.xAxes.push(new am4charts.CategoryAxis());
xAxis.dataFields.category = "x";
xAxis.renderer.grid.template.disabled = true;
xAxis.renderer.labels.template.disabled = true;
xAxis.tooltip.disabled = true;

var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
yAxis.min = 0;
yAxis.max = 1.99;
yAxis.renderer.grid.template.disabled = true;
yAxis.renderer.labels.template.disabled = true;
yAxis.renderer.baseGrid.disabled = true;
yAxis.tooltip.disabled = true;


// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.categoryX = "x";
series.dataFields.valueY = "y";
series.strokeWidth = 4;
series.sequencedInterpolation = true;

var bullet = series.bullets.push(new am4charts.CircleBullet());
bullet.setStateOnChildren = true;
bullet.states.create("hover");
bullet.circle.radius = 10;
bullet.circle.states.create("hover").properties.radius = 15;

var labelBullet = series.bullets.push(new am4charts.LabelBullet());
labelBullet.setStateOnChildren = true;
labelBullet.states.create("hover").properties.scale = 1.2;
labelBullet.label.text = "{text}";
labelBullet.label.maxWidth = 150;
labelBullet.label.wrap = true;
labelBullet.label.truncate = false;
labelBullet.label.textAlign = "middle";
labelBullet.label.paddingTop = 20;
labelBullet.label.paddingBottom = 20;
labelBullet.label.fill = am4core.color("#999");
labelBullet.label.states.create("hover").properties.fill = am4core.color("#000");

labelBullet.label.propertyFields.verticalCenter = "center";


chart.cursor = new am4charts.XYCursor();
chart.cursor.lineX.disabled = true;
chart.cursor.lineY.disabled = true;
        """
        # data = [{"x": "1","y": 1,"text": "[bold]2018 Q1[/]\nAAAA There seems to be some furry animal living in the neighborhood.", "center": "bottom"}, {
        #           "x": "2",
        #           "y": 1,
        #           "text": "[bold]2018 Q2[/]\nWe're now mostly certain it's a fox.",
        #           "center": "top"
        #         }, {
        #           "x": "3",
        #           "y": 1,
        #           "text": "[bold]2018 Q3[/]\nOur dog does not seem to mind the newcomer at all.",
        #           "center": "bottom"
        #         }, {
        #           "x": "4",
        #           "y": 1,
        #           "text": "[bold]2018 Q4[/]\nThe quick brown fox jumps over the lazy dog.",
        #           "center": "top"
        #         }];
            am_charts.exec_js(js_code)
            am_charts.assign_variable_js('window.chart.data', data)
            return am_charts.send_screenshot_to_slack(team_id, channel,clip=clip)
            #return "ok {0}".format(data)
        except Exception as error:
            return "error: {0}".format(error)

