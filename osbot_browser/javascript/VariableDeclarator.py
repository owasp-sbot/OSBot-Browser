from osbot_browser.javascript.Base_Node import Base_Node
from osbot_browser.javascript.Identifier import Identifier
from osbot_browser.javascript.Literal import Literal
from osbot_utils.utils.Misc import list_set


class VariableDeclarator(Base_Node):

    def __init__(self, js_ast, all_nodes):
        super().__init__(js_ast, all_nodes)
        assert list_set(js_ast) == ['id', 'init', 'type']
        self.id                  = js_ast.get('id')
        self.init                = js_ast.get('init')
        self.id_node             = None
        self.init_node           = None
        self.name                = None
        self.value               = None

    def parse_node(self):
        self.id_node = self.process_node(self.id)
        if self.init:
            self.init_node = self.process_node(self.init)

        if type(self.id_node) is Identifier:                # todo: see what other types (if any) need to be supported here
            self.name = self.id_node.name
        if type(self.init_node) is Literal:
            self.value = self.init_node.value


    def __repr__(self):
        return f"{self.name} = {self.value}"