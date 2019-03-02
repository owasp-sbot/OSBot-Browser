import json

from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files
from utils.Json import Json


class Risk_Dashboard:
    def __init__(self):
        self.web_page    = '/gs/risk/risks-dashboard.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__),'../web_root')
        self.render_page = Render_Page(web_root=self.web_root)

    def browser(self):
        return self.render_page.api_browser.sync__setup_browser()

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
        color   = '#{0}{0}{1}{1}00'.format('FEDCBA9876543210'[index], 'FEDCBA9876543210'[16 - index])
        css     = {'background-color': color}
        js_code = "$('#{0}').css({1})".format(r2_id, json.dumps(css))
        #self.js_eval(js_code)
        js_codes.append(js_code)
        return self