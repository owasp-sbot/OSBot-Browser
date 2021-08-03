from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class WhileStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['body', 'test', 'type']
        self.body                = js_ast.get('body')
        self.test                = js_ast.get('test')

    def parse_node(self):
        self.process_node (self.body )
        self.process_node (self.test)