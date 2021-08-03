from osbot_browser.javascript.Base_Node import Base_Node
from osbot_utils.utils.Misc import list_set


class TryStatement(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['block', 'finalizer', 'guardedHandlers', 'handler', 'handlers', 'type']
        self.block                = js_ast.get('block')
        self.finalizer            = js_ast.get('finalizer')
        self.guardedHandlers      = js_ast.get('guardedHandlers')
        self.handler              = js_ast.get('handler')
        self.handlers             = js_ast.get('handlers')

    def parse_node(self):
        if self.finalizer:
            self.process_node(self.finalizer)
        self.process_node (self.block )
        self.process_nodes(self.guardedHandlers )
        self.process_node (self.handler)
        self.process_nodes(self.handlers)