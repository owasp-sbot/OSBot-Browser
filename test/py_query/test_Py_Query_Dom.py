from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Misc import list_set

from osbot_browser.py_query.Py_Query import py_query_from_GET, Py_Query
from osbot_browser.py_query.Py_Query_Dom import Py_Query_Dom


class test_Py_Query_Dom(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.py_query = py_query_from_GET('https://httpbin.org/')

    def setUp(self):
        self.py_query_dom = Py_Query_Dom(self.py_query)
        assert type(self.py_query_dom.py_query) is Py_Query
        assert self.py_query_dom.py_query.tag() == 'html'

    def test_dom(self):
        dom = self.py_query_dom.dom()
        assert list_set(dom)          == ['attributes', 'children', 'tag', 'text']
        assert dom['tag']             == 'html'
        assert len(dom['attributes']) == 1
        assert len(dom['children'  ]) == 2
        assert len(dom['text'      ]) == 1540

        children = dom['children']
        child_element = children[0]

        assert list_set(children) == [0,1]
        assert list_set(child_element) == ['attributes', 'children', 'tag', 'text']
        assert child_element['tag'] == 'head'
        assert len(child_element['attributes']) == 0
        assert len(child_element['children'  ]) == 6
        assert len(child_element['text'      ]) == 187

        assert child_element.get('children')[0].get('attributes') == {'charset': 'UTF-8'}

    @patch('builtins.print')
    def test_print(self, builtins_print):
        self.py_query_dom.print()
        print_calls = builtins_print.mock_calls
        assert len(print_calls) == 78
        assert print_calls[2] == call('====================== All child html elements ======================')