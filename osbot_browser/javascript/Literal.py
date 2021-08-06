from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class Literal(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)

        # Note this is the first one that I've seen that has two different set of list_set(js_ast)

        if list_set(js_ast)         == ['raw', 'regex', 'type', 'value']:
            assert list_set(js_ast) ==  ['raw', 'regex', 'type', 'value']
        else:
            assert list_set(js_ast) == ['raw', 'type', 'value']
        self.raw                = js_ast.get('raw')
        self.regex              = js_ast.get('regex')
        self.value              = js_ast.get('value')

    def parse_node(self):
        assert type(self.raw) == str

    def __repr__(self):
        return self.raw
        #return f"<Literal raw={self.raw} | value={self.value}>"
