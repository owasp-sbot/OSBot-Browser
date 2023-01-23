import networkx

from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql
from osbot_jira.api.graph.plotly.Plotly_ICicle import Plotly_ICicle
from osbot_jira.data.COLORS_BY_PROJECT import COLORS_BY_PROJECT
from osbot_plotly.render.Plotly_Network_Graph import Plotly_Network_Graph
from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import upper


class Network_Graph_For_Jira_Graph:

    def __init__(self, jira_graph_jql=None):
        self.jira_graph_jql       = jira_graph_jql or Jira_Graph_Jql()
        self.plotly_network_graph = Plotly_Network_Graph()
        self.title                = "Visualisation of a Jira_Graph"
        self.use_directed_graph   = False
        #self.jira_graph           = None
        self.nx_graph             = None
        self.root_id              = None
        self.on_add_nx_node       = None
        self.node_text_field      = 'Key' # Summary
        self.set_plotly_setting()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def is_tree(self):
        return networkx.is_tree(self.nx_graph)

    def set_jira_graph_jql(self, jira_graph_jql):
        self.jira_graph_jql = jira_graph_jql
        return self

    def set_node_text_field(self, node_text_field):
        self.node_text_field = node_text_field
        return self

    def set_on_add_nx_node(self, on_add_nx_node):
        self.on_add_nx_node = on_add_nx_node
        return self

    def set_title(self, value):
        self.title = value

        return self

    def show_nodes_and_edges_text(self, value):
        self.plotly_network_graph.show_nodes_texts = value
        self.plotly_network_graph.show_edges_texts = value
        return self

    def hide_nodes_and_edges_text(self):
        return self.show_nodes_and_edges_text(False)

    def set_layout_iterations(self, value):
        if value:
            self.plotly_network_graph.nx_spring_layout_iterations = value
        return self

    def set_plotly_setting(self):
        _ = self.plotly_network_graph
        _.jpg_scale                   = 2
        _.nx_spring_layout_iterations = 50
        _.nx_spring_layout_k          = 1       # 1
        _.pl_node_text_size           = 10
        _.pl_node_marker_color        = 'darkblue'
        _.pl_node_text_color          = 'darkblue'
        _.pl_node_marker_size         = 10
        _.pl_edge_text_color          = "blue"
        _.pl_edge_line_color          = "blue"
        _.pl_edge_text_size           = 5
        _.pl_edge_line_width          = 0.1
        _.show_nodes_markers          = True
        _.show_edges_lines            = True
        _.show_nodes_texts            = True
        _.show_edges_texts            = True
        _.on_add_node                 = self.on_add_node

    def on_add_node(self, node_add_args):
        #pprint(node_add_args)
        self.jira_graph_jql.api_jira.log_requests = True
        self.jira_graph_jql.jira_graph.get_nodes_issues()
        issues   = self.jira_graph_jql.jira_graph.issues
        jira_id  = node_add_args['nx_node_id']
        issue_data = issues.get(jira_id)
        if issue_data:
            project     = issue_data.get('Project')
            maker_color = COLORS_BY_PROJECT.get(project) or self.plotly_network_graph.pl_node_marker_color
            if  COLORS_BY_PROJECT.get(project) is None:
                print(f"no color for project '{project}'")
            node_add_args['node_text'         ] = issue_data.get(self.node_text_field)
            node_add_args['node_text_color'   ] = maker_color
            node_add_args['node_marker_color' ] = maker_color

    def new_nx_graph(self):
        if self.use_directed_graph:
            self.nx_graph = networkx.DiGraph()  # todo, understand the side effects of this
        else:
            self.nx_graph = networkx.Graph()
        return self.nx_graph

    def create_jira_graph(self, jql, link_types, depth):
        (self.jira_graph_jql.set_jql(jql)
             .set_link_types(link_types)
             .set_depth(depth)
             .render_jira_graph())
        return self

    # todo: remove then having better solution to cache the jira_graph_jql results
    #@cache_on_tmp(reload_data=True)
    def get_nodes_edges(self):
        return self.jira_graph_jql.jira_graph.nodes, self.jira_graph_jql.jira_graph.edges

    def create_networkx_graph(self): #, nodes, edges):
        self.new_nx_graph()
        nodes = self.jira_graph_jql.get_nodes()
        edges = self.jira_graph_jql.get_edges()
        issues = self.jira_graph_jql.get_issues()
        #self.nx_graph = networkx.Graph()

        nx_graph = self.nx_graph
        for node_id in nodes:
            text = issues.get(node_id,{}).get(self.node_text_field, node_id)
            kwargs_add_node = { "text": text}
            if self.on_add_nx_node:
                self.on_add_nx_node(node_id, issues, kwargs_add_node)
            nx_graph.add_node(node_id,**kwargs_add_node)

        for (from_id, link_type, to_id) in edges:
            nx_graph.add_edge(from_id,to_id, text=link_type)
        return self.nx_graph


    def create_jpg_from_graph(self):
        if self.nx_graph is None:
            self.create_networkx_graph()
        (self.plotly_network_graph.set_title(self.title)
             .create_jpg_from_nx_graph(self.nx_graph))
        return self

    # def create_png(self, issue_id):
    #
    #     return (self#.set_issue_id           (issue_id)
    #                 #.create_graph_from_issue()
    #                 .create_png_from_graph  ()
    #                 .slack_upload_png       ())

