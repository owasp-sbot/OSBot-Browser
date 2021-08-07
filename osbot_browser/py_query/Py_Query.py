import requests
from osbot_utils.utils.Json import json_parse

from osbot_utils.utils.Misc import base64_to_str, list_set

from osbot_browser.py_query.Py_Query_Dom import Py_Query_Dom
from osbot_utils.decorators.lists.index_by import index_by
from pyquery import PyQuery

class Py_Query:
    def __init__(self, html='', pyquery=None):
        self.original_html = html
        self.error         = None
        self.pyquery       = pyquery or self.set_pyquery_from_html(html)


    def attribute(self, key):
        return self.attributes().get(key)

    def attribute_base64(self, key):
        value = self.attributes().get(key)
        return base64_to_str(value)

    def attribute_base64_py_query(self, key):
        html = self.attribute_base64(key)
        return Py_Query(html)

    def attribute_base64_json(self, key):
        return json_parse(self.attribute_base64(key))

    @index_by
    def attributes(self):
        if self.pyquery is None:
            return []
        if self.single_element():
            return self.pyquery[0].attrib
        result = []
        for item in self.pyquery:
            result.append(item.attrib)
        return result

    def children(self, selector='*'):
        result = []
        if self.pyquery is not None:
            for pyquery in self.pyquery.children(selector).items():
                result.append(Py_Query(pyquery=pyquery))
        return  result

    def dom(self, show_attributes=True, use_children_node=True):
        return Py_Query_Dom(self, show_attributes=show_attributes, use_children_node=use_children_node).dom()

    def elements(self, selector='*'):
        if self.pyquery is None:
            return []
        return self.query(selector).items()

    def empty(self):
        return self.size() == 0

    def html(self):
        if self.pyquery:
            return self.outer_html()
        return ''

    def inner_html(self):
        if self.pyquery:
            return self.pyquery.html()
        return ''

    def items(self):
        result = []
        if self.pyquery:
            for item in self.pyquery.items():
                result.append(Py_Query(pyquery=item))
        return result

    def indexed_by_attribute(self, attribute_name, return_unique_list=False):
        result = {}
        items = self.items()
        for item in items:
            attribute_value = item.attribute(attribute_name)
            if attribute_value:
                result[attribute_value] = item
        if return_unique_list:
            return list_set(result)
        return result

    def print(self):
        return Py_Query_Dom(self).print()

    def outer_html(self):
        if self.pyquery:
            return self.pyquery.outer_html()
        return ''

    def query(self, selector='*'):
        if self.pyquery:
            try:
                self.error = None
                pyquery = self.pyquery(selector)
                return Py_Query(pyquery=pyquery)
            except Exception as error:
                self.error = error
                return Py_Query('')

    def query_html(self, selector='*'):
        return self.query(selector=selector).html()

    def set_pyquery_from_html(self, html):
        self.pyquery = None
        self.error   = None
        if type(html) is str:
            try:
                self.pyquery = PyQuery(html)
                return self.pyquery
            except Exception as error:
                self.error = error
        else:
            self.error = Exception("Invalid html value")

    def size(self):
        if self.pyquery:
            return len(self.pyquery)
        return 0

    def set_value(self, selector, value):
        if self.pyquery:
            matches = []
            for item in self.query(selector).items():
                item.value(value)
                matches.append(item)
            return matches
            #target = self.query(selector)
            #return self.pyquery(selector).val(value)
        return []

    def single_element(self):
        return self.size() == 1

    def serialize_to_form(self):
        return self.pyquery.serialize()

    def scripts(self):                          # todo: move to separate class (one more focused the page's content)
        return self.query('script').indexed_by_attribute('src')

    def tag(self):
        if self.size() == 0:
            return ''
        return self.pyquery[0].tag # todo double check the use of [0] in the code below

    def tags(self):
        result = []
        if self.pyquery is not None:
            for item in self.pyquery:
                result.append(item.tag)
        return result

    def text(self,selector=None):
        if self.pyquery:
            if selector:
                return self.query(selector).text()
            return self.pyquery.text()
        return ''

    def value(self, value=None):
        if self.pyquery:
            if value:
                self.pyquery.val(value)
        return self

    def __repr__(self):
        return f'(Py_Query) tag: { self.tag()} | size: {self.size()} | attributes: {len(self.attributes())} | elements: {len(self.elements())} | children: {len(self.children())} \n\n {self.html()}'


    # todo: move to separate class (one more focused the page's content)
    # misc html helpers and page content

    def body(self):
        return self.query('body')

    def title(self):
        return self.text('title')


def py_query_from_html(html):                # allows to handle the case when html is or an error is raise my PyQuery
    return Py_Query(html=html)

def py_query_from_GET(url):
    response = requests.get(url)
    return Py_Query(response.text)

