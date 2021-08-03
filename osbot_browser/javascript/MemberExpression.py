from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class MemberExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['computed', 'object', 'property', 'type']
        self.computed            = js_ast.get('computed')
        self.object              = js_ast.get('object')
        self.property            = js_ast.get('property')

    def parse_node(self):
        assert type(self.computed) is bool
        self.process_node(self.object  )
        self.process_node(self.property)