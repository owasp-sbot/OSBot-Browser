import base64
import json
from unittest import TestCase

from syncer import sync

from src.view_helpers.View_Examples import View_Examples
from src.view_helpers.View_Risk_Dashboard import Risk_Dashboard
from utils.Dev import Dev
from utils.Files import Files
from utils.Json import Json


class Test_risk_dashboard(TestCase):
    def setUp(self):
        self.reload_page    = False
        self.risk_dashboard = Risk_Dashboard().show_chrome().load_page(self.reload_page)
        self.browser = self.risk_dashboard.browser()
        #self.view_examples  = View_Examples()
        #self.browser        = self.view_examples.render_page.api_browser
        #self.browser.sync__close_browser()

    def test_get_dashboard_data(self):
        data = self.risk_dashboard.get_dashboard_data('gs-dashboard.json')
        assert len(data.get('data_R1s')) == 7

    def test_load_page(self):
        self.risk_dashboard.load_page()

    def test_set_table_values(self):
        data = self.risk_dashboard.get_dashboard_data('gs-dashboard.json')

        data_R1s = data.get('data_R1s')
        data_R2s = data.get('data_R2s')
        risks    = data.get('risks')

        params = { 'cells': len(data_R1s), 'rows' :len(data_R2s) , 'data_R1s': data_R1s, 'data_R2s': data_R2s, 'risks': risks}
        self.risk_dashboard.execute('create_risk_table', params)

    def test_set_table_values__random_data(self):
        params = self.risk_dashboard.get_test_params(1,10)
        self.risk_dashboard.execute('create_risk_table', params)

    def test_set_r2_color(self):
        self.test_set_table_values__random_data()

        row = 1
        js_codes = []
        for i in range(1,11):
            r2_id = "r{0}_{1}".format(row, i)
            self.risk_dashboard.js_apply_css_color( js_codes, r2_id, i)

        self.risk_dashboard.js_eval(js_codes)




        #self._load_page()
        #await self.browser.js_execute("window.r1_and_r2.create_data_cells(6,6,'.')")

    # def test_run_coffee_script(self):
    #     html = "<script type='text/coffeescript'>"
    #     #html = "<h1>123</h1>"
    #     encoded_text = base64.b64encode(html.encode()).decode()
    #     script = "$('body').append($(atob('{0}')))".format(encoded_text)
    #     Dev.pprint(script)
    #     self.risk_dashboard.js_execute(script)




