import json
from time import sleep

from osbot_aws.apis.Lambda import Lambda

from osbot_browser.browser.API_Browser             import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper   import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page             import Render_Page
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json  import Json
from pbx_gs_python_utils.utils.Misc  import Misc


class Risk_Dashboard:
    def __init__(self, headless=True):
        self.web_page    = '/gs/risk/risks-dashboard.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__),'../web_root')
        self.headless    = headless
        self.api_browser = API_Browser(self.headless,self.headless).sync__setup_browser()
        self.render_page = Render_Page(api_browser=self.api_browser, web_root=self.web_root)
        self.graph_name  = None
        self.jira_key    = None

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

    def js_apply_css_color(self, js_codes, r2_id, index,diff=None, show_diff_delta=False):
        # if index < 1:                                           # min value is 1
        #     index = 1                                           # since we start the rows on 1
        # if index > 15:                                          # max value can be bigger than 16
        #     index = 16                                          # since that is the size of the Hex digits
        # hex_values = 'FEDCBA9876543210'
        # color   = '#{0}{0}{1}{1}00'.format(hex_values[index - 1], hex_values[16 - index])   # get the color changing the RGB values (R = Red , G = Green)

        js_code = ""
        if diff is not None:
            if diff  > 0 : value = '+' + str(diff)
            if diff == 0 : value = '='
            if diff  < 0 : value = diff
            #value = ""
            badge_code = '<br><span class="badge badge-secondary">{0}</span>'.format(value)
            js_code += "if ($('#{0}').text() != '') {{ $('#{0}').append('{1}') }}".format(r2_id,badge_code)
            if show_diff_delta:
                index =  diff * 2 + 4

        if show_diff_delta and index == 4:
            index = None
        if index is not None:
            if index < 1     : index = 1
            if index > 9     : index = 9
            colors = ['darkred', '#DE4108', '#F7794B',
                      '#E67F0D', '#EA9639', '#FAAE28',
                      '#4F9300', 'green', 'darkgreen']
            color = colors[index - 1]
        else:
            color = "#555555"

        css = {'background-color': color}
        js_code += "if ($('#{0}').text() != '') {{ $('#{0}').css({1}) }}".format(r2_id, json.dumps(css))
        js_codes.append(js_code)

        return self


    def send_screenshot_to_slack(self, team_id=None, channel=None,with_diffs=False):
        png_file = self.create_dashboard_screenshot(with_diffs)
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)


    def send_graph_name_to_slack(self, team_id, channel):
        from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
        slack_message(":point_right: Created graph `{0}` from jira key `{1}`".format(self.graph_name, self.jira_key),[], channel,team_id)
        return self

    def create_dashboard_screenshot(self, with_diffs=False):
        if with_diffs:
            height = 560
        else:
            height = 465
        clip = {'x': 1, 'y': 1, 'width': 945, 'height': height}
        return self.browser().sync__screenshot(clip=clip)


    def create_dashboard_with_scores(self,scores, diffs=None,show_diff_delta=False):
        self.create_dashboard_with_R1_R2()
        rows = 6
        cells = 6


        js_codes = []
        for i in range(1, cells + 1):
            for j in range(1, rows + 1):
                r2_id = "r{0}_{1}".format(i, j)
                # if scores.get(r2_id):
                #     color = scores.get(r2_id)
                # else:
                #     color = 1
                color = scores.get(r2_id)
                if diffs and diffs.get(r2_id) is not None:
                    diff = color - diffs.get(r2_id)
                else:
                    diff = None
                self.js_apply_css_color(js_codes, r2_id, color,diff,show_diff_delta)

        self.js_eval(js_codes)
        return self

    def create_dashboard_with_R1_R2(self):
        self.load_page(False)

        data = self.get_dashboard_data('gs-dashboard.json')

        data_R1s = data.get('data_R1s')
        data_R2s = data.get('data_R2s')
        risks = data.get('risks')

        params = {'cells': len(data_R1s), 'rows': len(data_R2s), 'data_R1s': data_R1s, 'data_R2s': data_R2s,
                  'risks': risks}

        self.execute('create_risk_table', params)
        return data_R1s, data_R2s

    def create_dashboard_with_test_data(self):
        self.create_dashboard_with_R1_R2()
        rows = 6
        cells = 6


        js_codes = []
        for i in range(1, cells + 1):
            for j in range(1, rows + 1):
                r2_id = "r{0}_{1}".format(i, j)
                color = Misc.random_number(1, 5)
                #color = j
                self.js_apply_css_color(js_codes, r2_id, color)

        self.js_eval(js_codes)
        return self


    def create_dashboard_for_graph(self,graph_name, root_node):
        from osbot_browser.view_helpers.Vis_Js import Vis_Js
        self.graph_name = graph_name
        self.jira_key   = root_node

        payload     = {"graph_name": graph_name, 'destination_node': root_node}
        graph_paths = Lambda('gs.graph_paths').invoke(payload)

        self.create_dashboard_with_R1_R2()

        graph_data = Vis_Js().get_graph_data(graph_name)

        nodes = graph_data.get('nodes')

        colors_scores = {}
        for key, node in nodes.items():
            if node:
                if 'R2' in node.get('Labels'):
                    summary = node.get('Summary')
                    cell_key = ("r" + summary.split('-')[0].replace('.','_')).strip()
                    #Dev.pprint(graph_paths.get(key))

                    if graph_paths.get(key):
                        score    = len(graph_paths.get(key))
                        colors_scores[cell_key] = score
                    #Dev.pprint(score)
                    #Dev.pprint(key + '   ' + cell_key + '   ' + str(score) + '   ' + summary)

        #return colors_scores
        #Dev.pprint(colors_scores)

        js_codes = []
        for i in range(1, 7):
            for j in range(1, 7):
                r2_id = "r{0}_{1}".format(i, j)
                color = colors_scores.get(r2_id)
                self.js_apply_css_color(js_codes, r2_id, color)

        self.js_eval(js_codes)

        return self


    def create_dashboard_for_jira_key(self,jira_key):
        lambda_graph = Lambda('lambdas.gsbot.gsbot_graph')

        payload = { 'data': {}, "params": ['expand', jira_key, 9, 'delivered by,risks_up']}
        result           = lambda_graph.invoke(payload)
        graph_data       = json.loads(result)
        graph_name       = graph_data.get('graph_name')
        sleep(1.0)      # to give time for ELK to index
        return self.create_dashboard_for_graph(graph_name,jira_key)


    def calculate_score(self,scores, title):
        size = len(scores)
        min = size
        max = size * 8
        #print(min, max)
        score = 0
        for value in scores.values():
            score += value
            #print(value, score)
        score = int((score - size) / max * 100)
        print("The score for {0:23} {1:3} / 100".format(title, score))
        return score, size