import json

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from browser.Render_Page import Render_Page
from utils.Files import Files
from utils.Json import Json
from utils.Misc import Misc


class Risk_Dashboard:
    def __init__(self):
        self.web_page    = '/gs/risk/risks-dashboard.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__),'../web_root')
        self.api_browser = API_Browser().sync__setup_browser()
        self.render_page = Render_Page(api_browser=self.api_browser, web_root=self.web_root)

    def browser(self):
        return self.api_browser

    def get_dashboard_data(self, path):
        json_file = Files.parent_folder_combine(__file__, path)
        return Json.load_json(json_file)

    def get_test_params(self,cells, rows):
        params = {'cells': cells, 'rows': rows, 'data_R1s': {}, 'data_R2s': {}}
        for i in range(1, params.get('cells') + 1):
            header_id = 'r{0}'.format(i)
            params['data_R1s'][header_id] = header_id
        for j in range(1, params.get('cells') + 1):
            for i in range(1, params.get('rows') + 1):
                header_id = 'r{0}_{1}'.format(j, i)
                params['data_R1s'][header_id] = header_id
        return params

    def show_chrome(self):
        self.render_page.api_browser.headless   = False
        self.render_page.api_browser.auto_close = False
        return self

    def load_page(self,reload=False):
        if reload or self.web_page not in self.browser().sync__url():
            self.render_page.open_file_in_browser(self.web_page)
        return self

    def execute(self, method,params=None):
        self.js_execute('window.r1_and_r2.{0}'.format(method), params)
        return self

    def js_execute(self, name,params=None):
        return self.browser().sync_js_invoke_function(name,params)

    def js_eval(self, js_code):
        return self.browser().sync__js_execute(js_code)

    def js_apply_css_color(self, js_codes, r2_id, index):
        # if index < 1:                                           # min value is 1
        #     index = 1                                           # since we start the rows on 1
        # if index > 15:                                          # max value can be bigger than 16
        #     index = 16                                          # since that is the size of the Hex digits
        # hex_values = 'FEDCBA9876543210'
        # color   = '#{0}{0}{1}{1}00'.format(hex_values[index - 1], hex_values[16 - index])   # get the color changing the RGB values (R = Red , G = Green)
        if index < 1 : index = 1
        if index > 5 : index = 5
        colors = ['darkred','red','orange','darkgreen','green']
        color  = colors[index - 1]
        css     = {'background-color': color}
        js_code = "if ($('#{0}').text() != '') {{ $('#{0}').css({1}) }}".format(r2_id, json.dumps(css))
        js_codes.append(js_code)
        return self


    def send_screenshot_to_slack(self, team_id, channel):
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)

    def create_dashboard_screenshot(self):
        clip = {'x': 1, 'y': 1, 'width': 945, 'height': 465}
        return self.browser().sync__screenshot(clip=clip)

    def create_dashboard_with_test_data(self):
        self.load_page(True)

        data = self.get_dashboard_data('gs-dashboard.json')

        data_R1s = data.get('data_R1s')
        data_R2s = data.get('data_R2s')
        risks = data.get('risks')

        params = {'cells': len(data_R1s), 'rows': len(data_R2s), 'data_R1s': data_R1s, 'data_R2s': data_R2s, 'risks': risks}

        rows = 6
        cells = 6

        #params = self.get_test_params(cells,rows)
        self.execute('create_risk_table', params)


        js_codes = []
        for i in range(1, cells + 1):
            for j in range(1, rows + 1):
                r2_id = "r{0}_{1}".format(i, j)
                color = Misc.random_number(1, 5)
                #color = j
                self.js_apply_css_color(js_codes, r2_id, color)

        self.js_eval(js_codes)
        return self