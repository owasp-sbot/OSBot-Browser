class Base_Node:
    def __init__(self, js_ast, all_nodes):
        self.js_ast    = js_ast
        self.all_nodes = all_nodes
        self.node_type = js_ast.get('type')
        self.check_class_name_match_type()
        self.nodes_dom = []
        self.add_self_to_all_nodes()

    def add_self_to_all_nodes(self):
        all_nodes = self.all_nodes
        node_type = self.node_type
        node_dom  = self
        if all_nodes.get(node_type) is None:
            self.all_nodes[node_type] = []
        self.all_nodes[node_type].append(node_dom)

    def check_class_name_match_type(self):
        from osbot_browser.javascript.Globals import NOT_SUPPORTED_TYPE
        class_name = self.current_class_name()
        if class_name!= NOT_SUPPORTED_TYPE:
            assert class_name == self.node_type

    def current_class_name(self):
        return self.__class__.__name__

    def process_nodes(self, nodes_ast):
        results = []
        for node_ast in nodes_ast:
            results.append(self.process_node(node_ast))
        return results

    def process_node(self, node_ast):
        if node_ast:
            result = self.process_type(node_ast)
            self.nodes_dom.append(result)
            return result

    def process_type(self, js_ast):
        from osbot_browser.javascript.Globals import NOT_SUPPORTED_TYPE
        from osbot_browser.javascript.Globals import supported_types
        if js_ast is None:                                          # todo: refactor the code to check the class to use to an helper method
            js_type_parser = supported_types[NOT_SUPPORTED_TYPE]
        elif js_ast.get('type') is None:
            js_type_parser = supported_types[NOT_SUPPORTED_TYPE]
        else:
            js_type         = js_ast.get('type')
            js_type_parser  = supported_types.get(js_type) or supported_types[NOT_SUPPORTED_TYPE]
        dom_type_parser = js_type_parser(js_ast, self.all_nodes)
        dom_type_parser.parse_node()
        return dom_type_parser

    def parse_node(self):
        print(f'**** MISSING parse_node method for {self.node_type}')

    def __repr__(self):
        #return f"<{self.node_type}>"
        return f" << {self.node_type} \n" + f"    {self.nodes_dom} >>"