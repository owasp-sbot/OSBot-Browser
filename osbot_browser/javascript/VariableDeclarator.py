from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class VariableDeclarator(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['id', 'init', 'type']
        self.id                  = js_ast.get('id')
        self.init                = js_ast.get('init')

    def parse_node(self):
        self.process_node(self.id)              # todo: find better way to map these variables
        if self.init:
            self.process_node(self.init)