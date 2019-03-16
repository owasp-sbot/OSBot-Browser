from view_helpers.Base_View_Helper import Base_View_Helpers


class Go_Js(Base_View_Helpers):
    def __init__(self,headless=True):
        self.web_page = '/go-js/simple.html'
        super().__init__(web_page=self.web_page,headless=headless)

    def create_graph(self,nodes, edges,options):

        self.load_page(True)
        data = {
            "nodes":  nodes
                    ,
            "edges": edges
        }
        self.invoke_js("create_graph",data)
        if self.api_browser.sync__await_for_element('#animationFinished'):
            self.invoke_js("console.log", 'animationFinished ok')
        # myDiagram.model = new go.GraphLinksModel(
        # [
        #   { from: "Alpha", to: "Beta" },
        #   { from: "Alpha", to: "Gamma" },
        #   { from: "Beta", to: "Beta" },
        #   { from: "Gamma", to: "Delta" },
        #   { from: "Delta", to: "Alpha" }
        # ]);
