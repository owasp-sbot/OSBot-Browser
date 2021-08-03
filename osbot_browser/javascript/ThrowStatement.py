from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class ThrowStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['argument','type']
        self.argument            = js_ast.get('argument')

    def parse_node(self):
        self.process_node(self.argument )