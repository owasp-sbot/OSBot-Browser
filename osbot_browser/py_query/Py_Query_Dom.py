from osbot_utils.utils.Dev import pprint

class Py_Query_Dom:

    def __init__(self, py_query, show_attributes=True, use_children_node=True):
        self.py_query          = py_query
        self.show_attributes   = show_attributes
        self.use_children_node = use_children_node

    def map_element(self,element):
        if element is None:
            return {}
        item = { 'tag'        : element.tag() ,
                 'text'       : element.text()}
        if self.use_children_node:
            item['children'] = self.map_elements(element.children())
        else:
            for index, child in enumerate(element.children()):
                item[index] = self.map_element(child)

        if self.show_attributes:
            item['attributes'] = element.attributes()
        return item

    def map_elements(self,elements):
        result = {}
        if elements is not None:
            for index, element in enumerate(elements):
                result[index] = self.map_element(element)
        return result

    def dom(self):
        return self.map_element(self.py_query)

    def print(self):
        print("")
        print("")
        print(f"====================== All child html elements ======================")
        print("")
        def print_element(indent, element):
            tag        = element.get('tag')
            attributes = element.get('attributes')
            print(f"{' ' * indent}<{tag}> {attributes}")
            for index, child in element.get('children').items():
                print_element(indent + 4, child)

        print_element(0, element = self.dom())