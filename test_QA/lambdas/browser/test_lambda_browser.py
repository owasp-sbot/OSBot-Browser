import base64
import json
import unittest

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Misc import Misc

from browser.Browser_Commands import Browser_Commands
from lambdas.browser.lambda_browser import run
from pbx_gs_python_utils.utils.Dev          import Dev


class Test_Lambda_lambda_browser(unittest.TestCase):
    def setUp(self):
        self.lambda_browser = Lambda('lambdas.browser.lambda_browser')

    def _save_png_file(self, png_data):
        try:
            png_file = '/tmp/lambda_png_file.png'
            if png_data:
                with open(png_file, "wb") as fh:
                    fh.write(base64.decodebytes(png_data.encode()))
                Dev.pprint("Png data with size {0} saved to {1}".format(len(png_data),png_file))
        except Exception as error:
            Dev.print("[_save_png_file][Error] {0}".format(error))
            Dev.print(png_data)

    def test_invoke_directly(self):
        result = run({},{})
        assert result == '*Here are the `Browser_Commands` commands available:*'

    def test_invoke_directly_version(self):
        result = run({"params": ['version']},{})
        assert result == Browser_Commands.current_version

    def test_invoke(self):
        payload ={ "params" : []}
        result = self.lambda_browser.invoke(payload)
        assert result == '*Here are the `Browser_Commands` commands available:*'

    def test_markdown(self):
        #payload = {"params": ['markdown'] }
        markdown = Misc.random_string_and_numbers(prefix='# Created from Lambda ')
        payload  = {"params": ['markdown', markdown, " \n normal text"]}
        png_data = self.lambda_browser.invoke(payload)
        Dev.pprint(png_data)
        self._save_png_file(png_data)

    def test_screenshot(self):
        team_id = 'T7F3AUXGV'
        channel = 'DDKUZTK6X'
        url = 'https://www.google.co.uk/aaa'
        #url = 'https://news.bbc.co.uk/aaa'
        #url = 'http://visjs.org/'
        payload = {"params": ['screenshot', url,], 'data': {'channel':channel, 'team_id': team_id}}
        result = self.lambda_browser.invoke(payload)
        Dev.pprint(result)

    def test_list(self):
        payload = {"params": ['list']}
        result = self.lambda_browser.invoke(payload)
        assert result == 'Here are the current examples files:'

    def test_lambda_status(self):
        payload = {"params": ['lambda_status']}
        result = self.lambda_browser.invoke(payload)
        assert result == 'Here are the current status of the `graph` lambda function'

    def test_render__bootstrap_cdn(self):
        payload = {"params": ['render','/examples/bootstrap-cdn.html',0,0,600,50]}
        png_data = self.lambda_browser.invoke(payload)
        self._save_png_file(png_data)

    def test_render__cup_of_tea(self):
        payload = {"params": ['render','examples/wardley_map/cup-of-tea.html']}
        png_data = self.lambda_browser.invoke(payload)
        self._save_png_file(png_data)


    def test_elk(self):
        payload = {"params": ['elk','dashboards']}
        png_data = self.lambda_browser.invoke(payload)
        #Dev.pprint(png_data)
        self._save_png_file(png_data)

    @unittest.skip('hangs on request')
    def test_elk__dashboard_project(self):
        payload = {"params": ['elk', 'dashboard_project','GSSP-126']}
        png_data = self.lambda_browser.invoke(payload)
        # Dev.pprint(png_data)
        self._save_png_file(png_data)



    def test_risks(self):
        #payload = {"params": ['render','gs/risk/risks-dashboard.html']}
        payload = { "params" : ['risks' , 'GSSP-115']}
        png_data = self.lambda_browser.invoke(payload)
        Dev.pprint(png_data)
        self._save_png_file(png_data)

    @unittest.skip('needs fixing (api has moved since this test)')
    def test_vis_js(self):
        nodes = [{'id': '123', 'label': 'vis js\n via lambda'},
                 {'id': 'aaa', 'label': 'another node'}]
        edges = [{'from': '123', 'to': 'aaa'}]

        options = {'nodes': {'shape': 'box'}}
        data = {'nodes': nodes, 'edges': edges, 'options': options }

        payload = { "params" : ['vis_js', json.dumps(data)]}
        png_data = self.lambda_browser.update_with_src().invoke(payload)
        Dev.pprint(png_data)
        self._save_png_file(png_data)

    @unittest.skip('needs fixing (api has moved since this test)')
    def test_graph(self):
        graph_name = 'graph_XKW'        # 7 nodes
        graph_name = 'graph_MKF'        # 20 nodes

        view_name  = 'default'
        payload = {"params": ['graph', graph_name, view_name]}
        png_data = self.lambda_browser.update_with_src().invoke(payload)
        #Dev.pprint(png_data)
        self._save_png_file(png_data)

    def test_graph__view__node_label(self):
        graph_name = 'graph_XKW'        # 7 nodes
        #graph_name = 'graph_VKN'        # 20 nodes
        #graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)

        view_name  = 'node_label'
        label_key  = 'Status'
        payload = {"params": ['graph', graph_name, view_name,label_key]}
        png_data = self.lambda_browser.invoke(payload)
        #Dev.pprint(png_data)
        self._save_png_file(png_data)

    # todo: fix: it is throwing '_AttributeError("\'NoneType\' object has no attribute \'get\'",)_')
    def test_table(self):
        payload = {"params": ['table','graph_MKF', 'graph']}
        png_data = self.lambda_browser.invoke(payload)
        Dev.pprint(png_data)
        self._save_png_file(png_data)

    def test_issue(self):
        payload = {"params": ['table','graph_MKF', 'issue']}
        png_data = self.lambda_browser.invoke(payload)
        Dev.pprint(png_data)
        self._save_png_file(png_data)
