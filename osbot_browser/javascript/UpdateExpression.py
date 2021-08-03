from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class UpdateExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['argument', 'operator', 'prefix', 'type']
        self.argument           = js_ast.get('argument')
        self.operator           = js_ast.get('operator')
        self.prefix             = js_ast.get('prefix')

    def parse_node(self):
        assert type(self.operator) is str
        assert type(self.prefix  ) is bool
        self.process_node(self.argument)