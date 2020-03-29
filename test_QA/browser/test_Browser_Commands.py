import base64
import json
import unittest
from   unittest import TestCase

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Commands import Browser_Commands
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.Deploy import Deploy


class Test_Browser_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.browser_commands = Browser_Commands()
        self.team_id          = None #'T7F3AUXGV'
        self.channel          = None #'DDKUZTK6X' #''GDL2EC3EE'


    def test_list(self):
        result = self.browser_commands.list(None, None, None)
        assert result[0] == 'Here are the current examples files:'
        assert len(result[1][0].get('text').split('\n')) > 10
        #assert result == (, [{'text': ''}])


    def test_screenshot(self):
        #os.environ['OSX_CHROME'] = 'True'
        url = 'https://www.google.co.uk'
        self.browser_commands.screenshot(self.team_id, self.channel, [url])

    def test_slack(self):
        #os.environ['OSX_CHROME'] = 'True'
        params = ['random', 2000]
        self.result = self.browser_commands.slack(self.team_id, self.channel, params)

    @unittest.skip("needs server running locally")
    def test_screenshot__localhost(self):
        url = 'http://localhost:12345'
        png_data = self.browser_commands.screenshot(None, None, params = [url])
        self._save_png_data(png_data)

    @unittest.skip("has delay")
    def test_screenshot__with_delay(self):
        url   = "https://www.google.com"
        delay = 2
        png_data = self.browser_commands.screenshot(None, None, params=[url,delay])
        self._save_png_data(png_data)

    def test_render(self):
        params   = ['examples/wardley_map/cup-of-tea.html']
        png_data = self.browser_commands.render(None,None,params)

        Files.delete(self.png_file)
        self._save_png_data(png_data)
        assert Files.exists(self.png_file)

    @unittest.skip('hangs')
    def test_render__with_clip_params(self):
        #params = ['/examples/bootstrap-cdn.html'        ,0  ,0 ,500 ,50 ]
        params = ['examples/wardley_map/cup-of-tea.html',250,50,600 ,200]
        png_data = self.browser_commands.render(None,None,params)
        Files.delete(self.png_file)
        self._save_png_data(png_data)
        assert Files.exists(self.png_file)

    @unittest.skip('has delay')
    def test_render_with_delay(self):
        params   = ['go-js','2']
        png_data = self.browser_commands.render(None,None,params)
        #Dev.print(png_data)
        self._save_png_data(png_data)

    def test_markdown___no_params(self):
        result = self.browser_commands.markdown(None,None,None)
        self._save_png_data(result)
        #Dev.pprint(result)

    def test_markdown___with_params(self):
        params = ["# Created from unit test \n","2nd paragraph --- 123"]
        result = self.browser_commands.markdown(None,None,params)
        self._save_png_data(result)

    def test_risk(self):
        params = ['GSSP-6']
        params = ['GSSP-113']
        result = self.browser_commands.risks(params=params)
        self._save_png_data(result)

    def test_graph(self):
        graph_name = 'graph_XKW'
        params = [graph_name,'default']
        result = self.browser_commands.graph(params=params)
        Dev.pprint(result)
        self._save_png_data(result)

    def test_graph__view__node_label(self):
        graph_name = 'graph_DEQ'
        params = [graph_name,'node_label', 'Labels']
        result = self.browser_commands.graph(params=params)
        Dev.pprint(result)
        self._save_png_data(result)

    def test_am_charts(self):
        graph_name = 'graph_XKW'
        params = [graph_name,'default']
        result = self.browser_commands.am_charts(params=params)
        Dev.pprint(result)
        self._save_png_data(result)

    def test_viva_graph(self):
        graph_name = 'graph_XKW'
        graph_name = 'graph_7AN' # 74 nodes
        #graph_name = 'graph_HDS' # very large graph
        #graph_name = 'graph_37V' # with `1617` nodes and `2907` edges,
        #graph_name = 'graph_VQW'
        graph_name = 'graph_56M'
        params = [graph_name,'default']
        result = self.browser_commands.viva_graph(params=params)
        #Dev.pprint(result)
        self._save_png_data(result)

    def test_go_js(self):
        self.test_update_lambda()
        graph_name = 'graph_J2O'
        params = [graph_name,'default']
        result = self.browser_commands.go_js(params=params)
        Dev.pprint(result)
        #self._save_png_data(result)


    def test_table(self):
        #self.test_update_lambda()
        params =['issue','Person-1']
        result = self.browser_commands.table(params=params)
        Dev.pprint(result)

    def test_google_charts(self):
        Deploy().setup()

        channel = 'DJ8UA0RFT'
        self.browser_commands.google_charts(None, channel,['default'])
        #self.browser_commands.oss_today(None, channel)

    def test_vis_js(self):
        self.result = self.browser_commands.vis_js(params =[])

    def test_sow(self):
        result = self.browser_commands.sow(None, None,['view', 'SOW-135'])
        Dev.pprint(result)
        #self.browser_commands.oss_today(None, channel)


    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser()