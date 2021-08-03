from osbot_utils.utils.Http import GET

from osbot_browser.javascript.Program import Program
from osbot_utils.utils.Misc import list_set, unique

from pyjsparser import PyJsParser


class Javascript_Parser:
    py_js_parser : PyJsParser
    program      : Program

    def __init__(self):
        self.py_js_parser = PyJsParser()
        self.all_nodes    = {}
        self.js_ast       = None
        self.js_dom       = None
        self.error        = None

    def ast_from_py_js_parser(self, js_code):
        return self.py_js_parser.parse(js_code)

    def ast_to_dom(self):
        self.program = Program(js_ast=self.js_ast, all_nodes=self.all_nodes)
        self.program.parse_node()
        return self.program

    def process_js_code(self, js_code):
        try:
            self.error = None
            self.js_ast = self.ast_from_py_js_parser(js_code=js_code)
            self.js_dom = self.ast_to_dom()
        except Exception as error:
            self.error = error
        return self

    def all_nodes__stats(self):
        keys      = list_set(self.all_nodes)
        result    = {}
        all_nodes = self.all_nodes
        for key in keys:
            key_nodes = all_nodes[key]
            result[key] = { 'size': len(key_nodes) }
        return result

    def get_functions(self):
        node_id = "FunctionDeclaration"
        nodes = self.all_nodes.get(node_id)
        for node in nodes:
            name   = node.id
            print( f"- {name}   -   {node.params}")
        return nodes

    def get_literals(self):
        node_id = "Literal"
        nodes = self.all_nodes.get(node_id)
        for node in nodes:
            print(f"raw: {node.raw} | value: {node.value} | regex: {node.regex}")

    def function_names(self, min_name_size=0):
        node_id = "FunctionDeclaration"
        names   = []
        nodes = self.all_nodes.get(node_id)
        if nodes:
            for node in nodes:
                if node.id:
                    name = node.id.get('name')
                    if min_name_size < len(name):
                        names.append(name)
        return unique(names)

    def identifier_names(self, min_name_size=0):
        node_id = "Identifier"
        names = []
        nodes = self.all_nodes.get(node_id)
        for node in nodes:
            name = node.name
            if min_name_size < len(name):
                names.append(name)
        return unique(names)

    def literal_names(self, min_name_size=0, starts_with=None):
        node_id = "Literal"
        names   = []
        nodes = self.all_nodes.get(node_id)
        for node in nodes:
            name = node.raw
            if min_name_size < len(name):
                if starts_with is None or name.startswith(starts_with):
                    names.append(name)
        return unique(names)

    def var_names(self, min_name_size=0):
        node_id = "VariableDeclarator"
        names = []
        nodes = self.all_nodes.get(node_id)
        for node in nodes:
            name = node.id.get('name')
            if min_name_size < len(name):
                names.append(name)
        return unique(names)


def JS_Parser_from_url(url):
    js_code = GET(url)
    return Javascript_Parser().process_js_code(js_code)