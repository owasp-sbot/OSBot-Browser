from unittest import TestCase
from urllib.parse import urljoin

import pytest

from osbot_browser.javascript.Javascript_Parser import Javascript_Parser
from osbot_utils.testing.Duration import Duration

from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp

from osbot_utils.utils.Http import GET

from osbot_browser.py_query.Py_Query import py_query_from_GET

JS_SIMPLE_CODE_1 = "var answer = 6 * 7;"

class test_Javascript_Parser(TestCase):

    def setUp(self) -> None:
        self.test_js_code_1 = JS_SIMPLE_CODE_1
        self.test_js_code_2 = self.get_test_code_2()
        #self.test_js_code_3 = self.get_test_code_3()
        #self.test_js_code_4 = self.get_test_code_4()
        #self.test_js_code_5 = self.get_test_code_5()

    @cache_on_tmp()
    def get_test_code_2(self):
        base_url = 'https://httpbin.org/'
        py_query = py_query_from_GET('https://httpbin.org/')
        js_srcs = []
        for key in py_query.query('script').indexed_by_attribute('src'):
            js_srcs.append(urljoin(base_url, key))

        js_85k = js_srcs.pop()
        return GET(js_85k)

    # todo find test JS with the sizes below
    # @cache_on_tmp()
    # def get_test_code_3(self):
    #     url_36k = ""
    #     return GET(url_36k)
    #
    # @cache_on_tmp()
    # def get_test_code_4(self):
    #     url_85k = ""
    #     return GET(url_85k)
    #
    # @cache_on_tmp()
    # def get_test_code_5(self):
    #     url_697k = ""
    #     return GET(url_697k)

    def js_parser_for_code(self, js_code):
        javascript_parser = Javascript_Parser()
        javascript_parser.process_js_code(js_code)
        return javascript_parser

    def test_ast_from_py_js_parser(self):
        js_code      = "var answer = 6 * 7;"
        expected_ast = { "type": "Program",
                         "body": [{ "declarations": [ {  "type": "VariableDeclarator",
                                                        "id": { "type": "Identifier", "name": "answer" },
                                                        "init": { "type": "BinaryExpression",
                                                                  "operator": "*",
                                                                  "left": { "type": "Literal", "value": 6.0, "raw": "6" },
                                                                  "right": { "type": "Literal", "value": 7.0, "raw": "7" }} }
                                                    ],
                                   "kind": "var",
                                   'type': 'VariableDeclaration' },
                                  {'type': 'EmptyStatement'}]
                      }
        js_ast = Javascript_Parser().ast_from_py_js_parser(js_code)
        assert js_ast == expected_ast

    @pytest.mark.skip("todo: write test for this function (that uses larger js file)")
    def test_ast_to_dom(self):
        javascript_parser = Javascript_Parser()
        js_code           = self.test_js_code_3

        javascript_parser.process_js_code(js_code)
        stats = javascript_parser.all_nodes__stats()
        #pprint(stats)
        #javascript_parser.get_functions()
        #javascript_parser.get_literals()

    def test_ast_to_dom_multiple_files(self):
        print()
        print()
        def process_file(js_code):
            with Duration(print_result=False) as duration:
                javascript_parser = Javascript_Parser()
                javascript_parser.process_js_code(js_code=js_code)
                js_dom = javascript_parser.js_dom
            print(f"{duration.seconds()} seconds | JS Code: {len(js_code)} | JS_Dom: {len(str(js_dom))}")

        process_file(self.test_js_code_1)
        process_file(self.test_js_code_2)
        #process_file(self.test_js_code_3)
        #process_file(self.test_js_code_4)
        #process_file(self.test_js_code_5)

        # 0.0003 seconds | JS Code: 19     | JS_Dom: 241
        # 0.4842 seconds | JS Code: 85578  | JS_Dom: 129
        # 0.1555 seconds | JS Code: 36174  | JS_Dom: 2741
        # 0.2768 seconds | JS Code: 85139  | JS_Dom: 5341
        # 3.6960 seconds | JS Code: 696948 | JS_Dom: 13929

    def test_literal_names(self):
        js_code = self.test_js_code_1
        js_parser = self.js_parser_for_code(js_code)
        assert js_parser.literal_names(min_name_size=0) == ['6', '7']

    @pytest.mark.skip("todo: write test for this function (that uses larger js file)")
    def test_method_names(self):
        js_code = self.test_js_code_3
        js_parser = self.js_parser_for_code(js_code)
        assert len(js_parser.function_names(min_name_size=3)) == 25

    def test_var_names(self):
        js_code = self.test_js_code_1
        js_parser = self.js_parser_for_code(js_code)
        assert js_parser.var_names(min_name_size=0) == ['answer']