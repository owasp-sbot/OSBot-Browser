# import base64
# from unittest import TestCase
#
# from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
# from osbot_browser.view_helpers.Risk_Dashboard import Risk_Dashboard
# from osbot_utils.utils.Dev import Dev
#
# class Test_risk_dashboard(TestCase):
#
#     def setUp(self):
#         self.reload_page    = False
#         self.risk_dashboard = Risk_Dashboard().show_chrome().load_page(self.reload_page)
#         self.browser        = self.risk_dashboard.browser()
#         self.result         = None
#         self.png_data       = None
#
#     def tearDown(self):
#         if self.result is not None:
#             Dev.pprint(self.result)
#
#         if self.png_data:
#             self.png_file = '/tmp/lambda_png_file.png'
#             with open(self.png_file, "wb") as fh:
#                 fh.write(base64.decodebytes(self.png_data.encode()))
#                 Dev.pprint('Saved png file with size {0} to {1}'.format(len(self.png_data), self.png_file))
#
#     def test_get_dashboard_data(self):
#         data = self.risk_dashboard.get_dashboard_data('gs-dashboard.json')
#         assert len(data.get('data_R1s')) == 7
#
#     def test_load_page(self):
#         self.risk_dashboard.load_page()
#
#     def test_set_table_values(self):
#         data = self.risk_dashboard.get_dashboard_data('gs-dashboard.json')
#
#         data_R1s = data.get('data_R1s')
#         data_R2s = data.get('data_R2s')
#         risks    = data.get('risks')
#
#         params = { 'cells': len(data_R1s), 'rows' :len(data_R2s) , 'data_R1s': data_R1s, 'data_R2s': data_R2s, 'risks': risks}
#         self.risk_dashboard.execute('create_risk_table', params)
#
#     def test_set_table_values__random_data(self):
#         params = self.risk_dashboard.get_test_params(1,10)
#         self.risk_dashboard.execute('create_risk_table', params)
#
#
#     def test_create_dashboard_with_scores(self):
#         scores = {'r1_1': 1, 'r2_1': 2, 'r3_1': 3 , 'r4_1': None, 'r5_1': 5 , 'r6_1': 6 ,
#                   'r1_2': 4, 'r2_2': 5 ,'r3_2': 6 , 'r4_2': None, 'r5_2': 2 , 'r6_2': 7 ,
#                   'r1_3': 7, 'r2_3': 8 , 'r3_3': 9 , 'r4_3': None, 'r5_3': 3 , 'r6_3': 8 ,
#                              'r2_4': None, 'r3_4': None , 'r4_4': None, 'r5_4': 4 , 'r6_4': 9 ,
#                              'r2_5': None, 'r3_5': None , 'r4_5': None, 'r5_5': 5 ,
#                                         'r3_6': None , 'r4_6': None,                      }
#
#         self.risk_dashboard.create_dashboard_with_scores(scores)
#         png_data = self.risk_dashboard.send_screenshot_to_slack()
#         Browser_Lamdba_Helper().save_png_data(png_data)
#
#     def test_create_dashboard_with_scores__with_diff(self):
#         scores = {'r1_1': 1, 'r2_1': 2, 'r3_1': 3 , 'r4_1': 0, 'r5_1': 5 , 'r6_1': 6 ,
#                   'r1_2': 4, 'r2_2': 5 ,'r3_2': 6 , 'r4_2': 0, 'r5_2': 2 , 'r6_2': 7 ,
#                   'r1_3': 7, 'r2_3': 8, 'r3_3': 9 , 'r4_3': 0, 'r5_3': 3 , 'r6_3': 8 ,
#                              'r2_4': 0, 'r3_4': 0 , 'r4_4': 0, 'r5_4': 4 , 'r6_4': 9 ,
#                              'r2_5': 8, 'r3_5': 2 , 'r4_5': 8, 'r5_5': 5 ,
#                                         'r3_6': 3 , 'r4_6': 9,                      }
#
#         scores_B = {'r1_1': 1, 'r2_1': 1, 'r3_1': 1, 'r4_1': 4, 'r5_1': 1, 'r6_1': 6,
#                     'r1_2': 5, 'r2_2': 2, 'r3_2': 4, 'r4_2': 5, 'r5_2': 2, 'r6_2': 7,
#                     'r1_3': 4, 'r2_3': 0, 'r3_3': 1, 'r4_3': 6, 'r5_3': 3, 'r6_3': 8,
#                                'r2_4': 2, 'r3_4': 1, 'r4_4': 1, 'r5_4': 4, 'r6_4': 9,
#                                'r2_5': 1, 'r3_5': 1, 'r4_5': 1, 'r5_5': 5,
#                                           'r3_6': 1, 'r4_6': 1,  }
#
#         #scores = scores_B
#         #scores_B = None
#         self.risk_dashboard.create_dashboard_with_scores(scores,scores_B)
#         png_data = self.risk_dashboard.send_screenshot_to_slack()
#         Browser_Lamdba_Helper().save_png_data(png_data)
#
#
#     def test_create_dashboard_with_test_data(self):
#         result = self.risk_dashboard.create_dashboard_with_test_data()
#         png_data = self.risk_dashboard.send_screenshot_to_slack()
#         result = Browser_Lamdba_Helper().save_png_data(png_data)
#         Dev.pprint(result)
#
#     def test_create_dashboard_with_test_data(self):
#         result = self.risk_dashboard.create_dashboard_with_test_data()
#         png_data = self.risk_dashboard.send_screenshot_to_slack()
#         result = Browser_Lamdba_Helper().save_png_data(png_data)
#         Dev.pprint(result)
#
#     def test_create_dashboard_for_graph(self):
#         graph_name = 'graph_DGK'
#         root_node = 'GSSP-6'
#         #graph_name = 'graph_DAS'
#         #root_node = 'GSSP-29'
#         graph_name = 'graph_GSA'
#         root_node ='GSSP-112'
#         #graph_name = 'graph_OBY'
#         #root_node ='GSSP-119'
#         graph_name = 'graph_JIE'
#         root_node = 'GSP-92'
#         with_diffs = True
#         risk_dashboard = self.risk_dashboard.create_dashboard_for_graph(graph_name, root_node)
#         self.png_data = risk_dashboard.create_dashboard_screenshot(with_diffs)
#
#
#
#     def test_create_dashboard_for_jira_key(self):
#         jira_key = 'GSSP-118'
#         result = self.risk_dashboard.create_dashboard_for_jira_key(jira_key)
#         result = self.risk_dashboard.send_screenshot_to_slack(None,None)
#         Dev.pprint(result)
#
#
#
#         #self._load_page()
#         #await self.browser.js_execute("window.r1_and_r2.create_data_cells(6,6,'.')")
#
#     # def test_run_coffee_script(self):
#     #     html = "<script type='text/coffeescript'>"
#     #     #html = "<h1>123</h1>"
#     #     encoded_text = base64.b64encode(html.encode()).decode()
#     #     script = "$('body').append($(atob('{0}')))".format(encoded_text)
#     #     Dev.pprint(script)
#     #     self.risk_dashboard.js_execute(script)
#
#
#
#
