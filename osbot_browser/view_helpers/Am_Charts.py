from pbx_gs_python_utils.utils.Misc import Misc
from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Am_Charts(Base_View_Helpers):
    def __init__(self,headless=True, layout=None):
        if layout:
            self.web_page = '/am_charts/{0}.html'.format(layout)
        else:
            self.web_page = '/am_charts/main.html'

        super().__init__(web_page=self.web_page,headless=headless)


    def get_nodes_and_edges(self, graph_data,nodes=None,edges=None, text_field='Key', append_key_to_text=False):
        if nodes is None: nodes = []
        if edges is None: edges = []

        for key,issue in graph_data.get('nodes').items():
            if issue and issue.get('Summary'):
                text = issue.get(text_field)
                if append_key_to_text:
                    text += " | {0}".format(key)
                nodes.append({'key': key, 'text': text , 'color': Misc.get_random_color()})

        for edge in graph_data.get('edges'):
            edges.append({ 'from': edge[0], 'text' : edge[1] ,'to': edge[2] ,'color':  Misc.get_random_color()})
        return nodes,edges

    def create_graph(self,nodes=None, edges=None,options=None):

        self.load_page(True)

        # data = {
        #     "nodes":  nodes
        #             ,
        #     "edges": edges
        # }
        #self.invoke_js("create_graph",data)
        #if self.api_browser.sync__await_for_element('#animationFinished'):
        #    self.invoke_js("console.log", 'animationFinished ok')

