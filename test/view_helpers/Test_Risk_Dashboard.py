from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from view_helpers.Risk_Dashboard import Risk_Dashboard
from utils.Dev import Dev

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


    def test_create_dashboard_with_scores_1(self):
        scores = {'r1_1': 1, 'r2_1': 4, 'r3_1': 9 , 'r4_1': 4, 'r5_1': 1 , 'r6_1': 6 ,
                  'r1_2': 2, 'r2_2': 5 ,'r3_2': 10, 'r4_2': 5, 'r5_2': 2 , 'r6_2': 7 ,
                  'r1_3': 3, 'r2_3': 6, 'r3_3': 0 , 'r4_3': 6, 'r5_3': 3 , 'r6_3': 8 ,
                             'r2_4': 7, 'r3_4': 1 , 'r4_4': 7, 'r5_4': 4 , 'r6_4': 9 ,
                             'r2_5': 8, 'r3_5': 2 , 'r4_5': 8, 'r5_5': 5 ,
                                        'r3_6': 3 , 'r4_6': 9,                      }
        self.risk_dashboard.create_dashboard_with_scores(scores)
        png_data = self.risk_dashboard.send_screenshot_to_slack()
        #Dev.pprint(png_data)
        result = Browser_Lamdba_Helper().save_png_data(png_data)


    def test_create_dashboard_with_test_data(self):
        result = self.risk_dashboard.create_dashboard_with_test_data()
        png_data = self.risk_dashboard.send_screenshot_to_slack()
        result = Browser_Lamdba_Helper().save_png_data(png_data)
        Dev.pprint(result)

    def test_create_dashboard_with_test_data(self):
        result = self.risk_dashboard.create_dashboard_with_test_data()
        png_data = self.risk_dashboard.send_screenshot_to_slack()
        result = Browser_Lamdba_Helper().save_png_data(png_data)
        Dev.pprint(result)

    def test_create_dashboard_for_graph(self):
        graph_name = 'graph_DGK'
        root_node = 'GSSP-6'
        #graph_name = 'graph_DAS'
        #root_node = 'GSSP-29'
        graph_name = 'graph_GSA'
        root_node ='GSSP-112'
        #graph_name = 'graph_OBY'
        #root_node ='GSSP-119'
        graph_name = 'graph_JIE'
        root_node = 'GSP-92'
        result = self.risk_dashboard.create_dashboard_for_graph(graph_name, root_node)
        Dev.pprint(result)

    def test_create_dashboard_for_jira_key(self):
        jira_key = 'GSSP-118'
        result = self.risk_dashboard.create_dashboard_for_jira_key(jira_key)
        result = self.risk_dashboard.send_screenshot_to_slack(None,None)
        Dev.pprint(result)



        #self._load_page()
        #await self.browser.js_execute("window.r1_and_r2.create_data_cells(6,6,'.')")

    # def test_run_coffee_script(self):
    #     html = "<script type='text/coffeescript'>"
    #     #html = "<h1>123</h1>"
    #     encoded_text = base64.b64encode(html.encode()).decode()
    #     script = "$('body').append($(atob('{0}')))".format(encoded_text)
    #     Dev.pprint(script)
    #     self.risk_dashboard.js_execute(script)




