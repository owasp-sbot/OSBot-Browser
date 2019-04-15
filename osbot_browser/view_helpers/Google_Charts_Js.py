from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page import Render_Page
from pbx_gs_python_utils.utils.Files import Files


class Google_Charts_Js:

    def __init__(self):
        self.web_page     = '/google_charts/simple.html'
        self.web_root     = Files.path_combine(Files.parent_folder(__file__),'../web_root')
        self.api_browser  = API_Browser().sync__setup_browser()
        self.render_page  = Render_Page(api_browser=self.api_browser, web_root=self.web_root)
        self.table_width  = '100%'
        self.columns_defs = None
        self.table_title  = None

    # helper methods (to move to base class)
    def browser(self):
        return self.api_browser

    def show_chrome(self):
        self.render_page.api_browser.headless   = False
        self.render_page.api_browser.auto_close = False
        return self

    def load_page(self,reload=False):
        if reload or self.web_page not in self.browser().sync__url():
            self.render_page.open_file_in_browser(self.web_page)
        return self

    def js_execute(self, name,params=None):
        return self.browser().sync_js_invoke_function(name,params)

    def js_eval(self, js_code):
        return self.browser().sync__js_execute(js_code)

    def send_screenshot_to_slack(self, team_id, channel):
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)

    def create_dashboard_screenshot(self):
        #clip = {'x': 1, 'y': 1, 'width': 945, 'height': 465}
        clip = None
        return self.browser().sync__screenshot(clip=clip)

    # main datatable methods

    def create_data_table(self):#, cols, rows):

        cols = [{'id': 'task', 'label': 'Task', 'type': 'string'},
                {'id': 'hours', 'label': 'Hours per Day', 'type': 'number'}]
        rows = [{'c': [{'v': 'Work'}, {'v': 11} ]} ,
                {'c': [{'v': 'Play'}, {'v': 2  }]},
                {'c': [{'v': 'Other'}, {'v': 5}]}
                ]

        data = { 'cols' : cols, 'rows' : rows}
        options = {'title':'My first chart',
                   'width': 500,
                   'height':500  };
        chart_type = 'LineChart' #'BarChart' # PieChart'
        self.js_execute('window.data_table=new google.visualization.DataTable',data)
        self.js_execute('window.options = ', options)

        self.js_eval("""window.chart = new google.visualization.{0}(document.getElementById('chart_div'));
                        chart.draw(data_table, options);""".format(chart_type))
        #dt = new
        ##google.visualization.DataTable({
        #    cols:
