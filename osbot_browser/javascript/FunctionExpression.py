from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class FunctionExpression(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['body', 'defaults', 'expression', 'generator', 'id', 'params', 'type']
        self.body                = js_ast.get('body')
        self.defaults            = js_ast.get('defaults')
        self.expression          = js_ast.get('expression')
        self.generator           = js_ast.get('generator')
        self.id                  = js_ast.get('id')
        self.params              = js_ast.get('params')

    def parse_node(self):
        if self.id is not None:
            self.process_node(self.id)
        assert type(self.expression) is bool
        assert type(self.generator)  is bool

        self.process_node (self.body    )                      # todo: find a better way to capture
        self.process_nodes(self.defaults)
        self.process_nodes(self.params)
