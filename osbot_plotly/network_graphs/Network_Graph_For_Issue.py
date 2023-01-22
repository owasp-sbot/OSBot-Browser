import networkx

from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_plotly.render.Plotly_Network_Graph import Plotly_Network_Graph
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Misc import random_string, word_wrap, word_wrap_escaped


class Network_Graph_For_Issue:

    def __init__(self):
        self.api_jira_rest        = API_Jira_Rest()
        self.plotly_network_graph = Plotly_Network_Graph()
        self.issue_id             = None
        self.graph                = None
        self.title                = None


    def create_graph_from_issue(self):
        with Duration(prefix=' > create_graph_from_issue', print_result=False):
            issue       = self.api_jira_rest.issue(self.issue_id)
            self.graph  = networkx.Graph()
            graph       = self.graph
            root_id     = random_string()
            graph.add_node(root_id, text_size=15, color='black', value=self.issue_id)
            for name, value in issue.items():
                name_id = random_string()
                graph.add_node(name_id, text_size=10, color='blue', value=name)
                graph.add_edge(root_id,name_id)

                if name == 'Issue Links':
                    value_id = random_string()
                    graph.add_node(value_id, text_size=7, color='green', value=name)
                    graph.add_edge(name_id, value_id)
                    for link_type, link_ids in value.items():
                        graph.add_node(link_type, text_size=7, color='black', value=link_type)
                        graph.add_edge(value_id, link_type)
                        for link_id in link_ids:
                            link_id_id = random_string()
                            graph.add_node(link_id_id, text_size=7, color='gray', value=link_id)
                            graph.add_edge(link_type, link_id_id)
                    pass
                else:
                    value_id     = random_string()
                    value_subset = str(value)[0:30]
                    graph.add_node(value_id,text_size=7, color='green', value=value_subset)
                    graph.add_edge(name_id, value_id)

        return self

    def create_png_from_graph(self):
        (self.plotly_network_graph.set_title(self.title)
             .create_jpg_from_nx_graph(self.graph))
        return self

    def set_issue_id(self, issue_id):
        self.issue_id = issue_id
        self.title = f"Graph for issue_id: {self.issue_id}"
        return self


    def create(self, issue_id):
        return (self.set_issue_id(issue_id)
                .create_graph_from_issue()
                .create_png_from_graph())
