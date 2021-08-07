from unittest import TestCase

import lxml
import pyquery
from lxml.etree import ParserError
from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Dev import pprint
from pyquery import PyQuery

from osbot_browser.py_query.Py_Query import Py_Query, py_query_from_html


class test_Py_Query(TestCase):

    def setUp(self) -> None:
        self.test_html   = "<html>" \
                                "<head id='abc' answer='42'>" \
                                    "inside <b>head</b>" \
                                "</head>" \
                               "<body>" \
                                    "in the body" \
                                    "<div id='1'>1</div>"   \
                                    "<div id='2'>2</div>"   \
                                    "<span id='3'>3</span>" \
                               "</body>" \
                           "</html>"
        self.py_query = Py_Query(html=self.test_html)

    def test__init__(self):
        assert type(self.py_query).mro()          == [Py_Query, object]
        assert type(self.py_query.html()).mro()   == [str, object                          ]
        assert type(self.py_query.pyquery).mro() == [pyquery.pyquery.PyQuery, list, object]
        assert self.py_query.html()               == self.test_html.replace("'",'"')


    def test__init__with_empty_or_bad_values(self):
        assert str(Py_Query(''  ).error) == str(ParserError('Document is empty'))
        assert str(Py_Query(None).error) == str(Exception("Invalid html value"))
        assert str(Py_Query(-1  ).error) == str(Exception("Invalid html value"))
        assert Py_Query('a' ).error is None
        assert Py_Query('<>').error is None
        assert Py_Query('{}').error is None
        py_query = Py_Query('')

        assert py_query.attributes    () == []
        assert py_query.children      () == []
        assert py_query.dom           () == {'attributes': [], 'children': {}, 'tag': '', 'text': ''}
        assert py_query.elements      () == []
        assert py_query.empty         () is True
        assert py_query.inner_html    () == ''
        assert py_query.html          () == ''
        assert py_query.items         () == []
        assert py_query.outer_html    () == ''
        assert py_query.size          () == 0
        assert py_query.single_element() is False
        assert py_query.tag           () == ''
        assert py_query.tags          () == []
        assert py_query.text          () == ''
        assert py_query.query         () is None

        assert str(py_query.error) == str(ParserError('Document is empty'))
        py_query.error = None
        assert py_query.set_pyquery_from_html('') is None
        assert str(py_query.error) == str(ParserError('Document is empty'))
        assert py_query.set_pyquery_from_html(None) is None
        assert str(py_query.error) == str(Exception("Invalid html value"))

        assert py_query.query                 ('html'         ) is None
        assert type(py_query.set_pyquery_from_html ('<html/>')) is PyQuery
        assert type(py_query.query            ('html'        )) is Py_Query

        #assert py_query.error.message == 's'
        #pprint(py_query.pyquery_from_html(''))

    def test__pyquery_methods(self):
        py_query = self.py_query.pyquery
        #pprint(dir(self.py_query.py_query))
        assert py_query.base_url is None
        assert py_query.count("head") == 0
        assert len(py_query.contents())  == 2

        element = py_query.contents()[0]
        assert type(element).mro()      == [lxml.etree._Element, object]
        assert element.keys()           == ['id', 'answer']
        assert element.tag              == 'head'
        assert type(element.itertext()) == lxml.etree.ElementTextIterator
        assert element.text             == 'inside '
        assert element.values()         == ['abc', '42']

        assert list(py_query.items()) == [py_query]
        #pprint(py_query.make_links_absolute())     # todo: add use case (needs baseUrl)
        assert py_query.text() == 'inside head\nin the body\n1\n2\n3'
        #pprint(py_query.xhtml_to_html())           # todo: figure if this PyQuery feature is useful


    # Py_Query

    def test_attributes(self):
        assert self.py_query.attributes() == {}
        assert self.py_query.query('aaaa').attributes() == []
        assert self.py_query.query('html').attributes() == []
        assert self.py_query.query('head').attributes() == {'id': 'abc', 'answer': '42'}
        assert self.py_query.query('div' ).attributes() == [{'id': '1'}, {'id': '2'}]


    def test_dom(self):
        body = self.py_query.query('html')
        dom = body.dom()
        assert dom.get('tag') == 'html'
        assert len(dom.get('children')) == 2
        assert dom.get('children')[0].get('tag') == 'head'
        assert dom.get('children')[0].get('text') == 'inside head'
        #pprint(dom)

    def test_elements(self):
        all_elements = self.py_query.elements()
        assert len(all_elements) == 7
        for element in all_elements:
            assert type(element) == Py_Query

    def test_tags(self):
        assert self.py_query             .tags() == ['html']
        assert self.py_query.query('div').tags() == ['div', 'div']
        assert self.py_query.query(''   ).tags() == []
        assert self.py_query.query(None ).tags() == []
        assert self.py_query.query('aaa').tags() == []

    def test_serialize_to_form(self):
        random_value = random_string()
        html = f'<form><input name="order" value="{random_value}">'          \
               '<input name="order2" value="baked beans"></form>'
        py_query = Py_Query(html)
        assert py_query.serialize_to_form() == f'order={random_value}&order2=baked%20beans'

    def test_query(self):
        query = self.py_query.query('head')
        assert type(query) == Py_Query

        assert query.outer_html() == '<head id="abc" answer="42">inside <b>head</b></head>'

        children = query.children()
        assert children[0].html() == '<b>head</b>'

        elements = query.elements()
        assert type(elements[0]) == Py_Query
        pprint(type(elements))
        assert type(elements).mro() == [list, object]



        element = elements[0]
        assert type(element).mro()  == [Py_Query, object]
        assert element.text()       == 'inside head'
        assert element.attributes() == {'id': 'abc', 'answer': '42'}

        assert type(elements[0]       ) == Py_Query
        assert type(element.items()[0]) is Py_Query       # confirm that .items returns an Py_Query object

        # couple more pyquery tests
        assert query.set_pyquery_from_html('<form><input name="order" value="spam"></form>').serialize_array() == [{'name': 'order', 'value': 'spam'}]

        # todo: add tests for the PyQuery features below (which look quite interesting)
        #       https://pyquery.readthedocs.io/en/latest/api.html
        # filter
            # >>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p>')
            # >>> d('p')
            # [<p.hello>, <p>]
            # >>> d('p').filter('.hello')
            # [<p.hello>]
            # >>> d('p').filter(lambda i: i == 1)
            # [<p>]
            # >>> d('p').filter(lambda i: PyQuery(this).text() == 'Hi')
            # [<p.hello>]
            # >>> d('p').filter(lambda i, this: PyQuery(this).text() == 'Hi')
            # [<p.hello>]
        # find
            # >>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
            # >>> d = PyQuery(m)
            # >>> d('p').find('em')
            # [<em>, <em>]
            # >>> d('p').eq(1).find('em')
            # [<em>]
        # map
            # >>> d = PyQuery('<p class="hello">Hi there</p><p>Bye</p><br />')
            # >>> d('p').map(lambda i, e: PyQuery(e).text())
            # ['Hi there', 'Bye']
            #
            # >>> d('p').map(lambda i, e: len(PyQuery(this).text()))
            # [8, 3]
            #
            # >>> d('p').map(lambda i, e: PyQuery(this).text().split())
            # ['Hi', 'there', 'Bye']
        # serialise (for Forms)
            # >>> h = (
            # ... '<form><input name="order" value="spam">'
            # ... '<input name="order2" value="baked beans"></form>'
            # ... )
            # >>> d = PyQuery(h)
            # >>> d.serialize()
            # 'order=spam&order2=baked%20beans'

    def test_Py_Query_from_html(self):
        py_query = py_query_from_html('<html>aaa</html>')
        assert type(py_query) is Py_Query
        assert py_query.html() == '<html>aaa</html>'
        empty_py_query = py_query_from_html('')
        assert str(empty_py_query.error) == str(ParserError('Document is empty'))