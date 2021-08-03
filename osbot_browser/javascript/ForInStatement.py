from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class ForInStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['body', 'each', 'left', 'right', 'type']
        self.body                = js_ast.get('body')
        self.each                = js_ast.get('each')
        self.left                = js_ast.get('left')
        self.right               = js_ast.get('right')

    def parse_node(self):
        assert type(self.each) is bool
        self.process_node(self.each )
        self.process_node(self.left )
        self.process_node(self.right)