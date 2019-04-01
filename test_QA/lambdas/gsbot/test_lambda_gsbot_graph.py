import  unittest

from    pbx_gs_python_utils.utils.Dev              import Dev
from    pbx_gs_python_utils.utils.aws.Lambdas      import Lambdas


class test_lambda_gsbot_graph(unittest.TestCase):
    def setUp(self):
        self.lambda_graph = Lambdas('lambdas.gsbot.gsbot_graph',memory=3008)

    def test_update(self):
        self.lambda_graph.update_with_src()

    # def test_update_both(self):
    #     Lambdas('pbx_gs_python_utils.lambdas.gsbot.gsbot_graph'     ).update_with_src()
    #     Lambdas('pbx_gs_python_utils.lambdas.pbx_gs_python_utils.lambdas.gs.elastic_jira').update_with_src()

    def update_and_invoke(self, command):
        payload = {
            "params": command.split(' '),
            "data": {"channel": "DDKUZTK6X", 'team_id' : 'T7F3AUXGV'}
        }
        return self.lambda_graph.update_with_src().invoke(payload)

    def invoke(self, command):
        payload = {
            "params": command.split(' '),
            "data": {"channel": "DDKUZTK6X", 'team_id' : 'T7F3AUXGV'}
        }
        return self.lambda_graph.invoke(payload)



    def test_update_invoke(self):
        payload =  {
                        "params": [],
                        "data"  : { "channel" : "DDKUZTK6X" , 'team_id' : 'T7F3AUXGV'}
                    }
        result = self.lambda_graph.update_with_src().invoke(payload)
        Dev.pprint(result)

    def test_invoke___last(self):
        Dev.print(self.update_and_invoke('last 20'))

    def test_invoke___show_last(self):
        self.update_and_invoke('show_last 1')

    def test_invoke___save(self):
        self.update_and_invoke('save 1 test-save')

    def test_nodes_add_node(self):
        self.update_and_invoke('nodes add_node graph_T28 RISK-443')

    def test_nodes_add_edge(self):
        self.update_and_invoke('nodes add_edge graph_WLA GSP-1 connects_to GSP-95')

    def test_story_jira_sec_9195(self):
        self.update_and_invoke('story_jira_sec_9195')

    def test_story_jira_sec_9195___stakeholders(self):
        self.update_and_invoke('story_jira_sec_9195 stakeholders')

    def test_story_jira_sec_9195___stakeholders__id(self):
        self.update_and_invoke('story_jira_sec_9195 stakeholder GSP-73')

    def test_story_jira_sec_9195___stakeholders__id_depth(self):
        self.update_and_invoke('story_jira_sec_9195 stakeholder GSP-73 1')

    def test_story__id(self):
        self.update_and_invoke('story sec-47-up')

    def test_story__id_stakeholders(self):
        self.update_and_invoke('story sec-47-up stakeholders')

    def test_story__story_id___stakeholder___stakeholder_id(self):
        self.update_and_invoke('story sec-47-up stakeholder GSP-1 2')


    def test_story__story_id___stakeholder___stakeholder_id__babel_admins(self):
        self.invoke('story babel-admin-vuln stakeholder GSP-4 2')


    def test_expand___abc(self):
        Dev.print(self.update_and_invoke('expand abc'))

    def test_raw_data(self):
        result = self.update_and_invoke('raw_data graph_MKF details')
        Dev.print(result)

    def test_raw_data__details(self):
        result = self.update_and_invoke('raw_data graph_MKF')
        Dev.print(result)

    def test_raw_data__issue_id(self):
        result = self.update_and_invoke('raw_data GSSP-111 details')
        Dev.print(result)

    def test_update_with_src__refactor_test(self):
        result = self.lambda_graph.update_with_src().invoke({ 'params': ['refactor_test']})
        Dev.pprint(result)


    def test_update_lambdas(self):
        Lambdas('gsbot.gsbot_graph').update_with_src()
        Lambdas('pbx_gs_python_utils.lambdas.gs.elastic_jira').update_with_src()