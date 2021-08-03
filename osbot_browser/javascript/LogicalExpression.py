from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class LogicalExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['left', 'operator', 'right', 'type']
        self.left = js_ast.get('left')
        self.operator = js_ast.get('operator')
        self.right = js_ast.get('right')

    def parse_node(self):
        assert type(self.operator) is str
        self.process_node(self.left)
        self.process_node(self.right)