from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class CallExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['arguments', 'callee', 'type']
        self.arguments           = js_ast.get('arguments')
        self.callee              = js_ast.get('callee')


    def parse_node(self):
        self.process_nodes(self.arguments )                      # todo: find a better way to capture
        self.process_node (self.callee)                          #       this calle and arguments relationship