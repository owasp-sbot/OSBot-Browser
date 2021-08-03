from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class SwitchStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['cases', 'discriminant', 'type']
        self.cases = js_ast.get('cases')
        self.discriminant = js_ast.get('discriminant')

    def parse_node(self):
        self.process_nodes(self.cases)
        self.process_node (self.discriminant)
