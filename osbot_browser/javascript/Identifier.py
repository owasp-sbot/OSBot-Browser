from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class Identifier(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['name', 'type']
        self.name                = js_ast.get('name')

    def parse_node(self):
        assert type(self.name) == str
        pass

    def __repr__(self):
        return f"<Identifier name={self.name}>"
