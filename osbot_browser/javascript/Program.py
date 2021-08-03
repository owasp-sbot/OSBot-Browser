from osbot_browser.javascript.Base_Node import Base_Node


class Program(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        self.body  = js_ast.get('body')

    def parse_node(self):
        self.process_nodes(self.body)