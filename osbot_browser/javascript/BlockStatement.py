from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class BlockStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['body','type']
        self.body                = js_ast.get('body')

    def parse_node(self):
        self.process_nodes(self.body )