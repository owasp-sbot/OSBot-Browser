from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class ConditionalExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['alternate', 'consequent', 'test', 'type']
        self.alternate           = js_ast.get('alternate')
        self.consequent          = js_ast.get('consequent')
        self.test                = js_ast.get('test')

    def parse_node(self):
        self.process_node(self.alternate )                      # todo: find a better way to capture
        self.process_node(self.consequent)
        self.process_node(self.test      )