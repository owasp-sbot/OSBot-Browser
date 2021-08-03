from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class Property(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['computed', 'key', 'kind', 'method', 'shorthand', 'type', 'value']
        self.computed            = js_ast.get('computed')
        self.key                 = js_ast.get('key')
        self.kind                = js_ast.get('kind')
        self.method              = js_ast.get('method')
        self.shorthand           = js_ast.get('shorthand')
        self.value               = js_ast.get('value')


    def parse_node(self):
        assert type(self.computed ) is bool
        assert type(self.kind     ) is str
        assert type(self.method   ) is bool
        assert type(self.shorthand) is bool

        self.process_node (self.key  )
        self.process_node (self.value)
