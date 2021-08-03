from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class BreakStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['label','type']
        self.label               = js_ast.get('label')

    def parse_node(self):
        pass

    # def __repr__(self):
    #     return f"<BreakStatement label={self.label}>"