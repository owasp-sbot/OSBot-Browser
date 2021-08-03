from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class ForStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['body', 'init', 'test', 'type', 'update']
        self.body                = js_ast.get('body')
        self.init                = js_ast.get('init')
        self.test                = js_ast.get('test')
        self.update              = js_ast.get('update')

    def parse_node(self):
        self.process_node(self.body  )
        self.process_node(self.init  )
        self.process_node(self.test  )
        if self.update:
            self.process_node(self.update)