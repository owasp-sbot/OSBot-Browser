from unittest import TestCase

from browser import Browser_Lamdba_Helper
from utils.Dev import Dev
from view_helpers.DataTable_Js import DataTable_Js


class Test_DataTable_Js(TestCase):

    def setUp(self):
        self.png_data   = None
        self.datatable_js = DataTable_Js()

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_load_page(self):
        self.datatable_js.load_page(True)


    def test_create_table(self):
        self.datatable_js.load_page(True)
        headers = ['Header AAA','Header BBB']
        rows    = [['value 1'  , 'value 2'  ],
                   ['value 3'  , 'value 4'  ],
                   ['value 5'               ],
                   [                        ],
                   ['value 6'  , 'value 7'  ],
                   [None                    ],
                   [None,'value 8', 'AB'    ],
                   ['value 9'  , 'value 10' ]]

        html = self.datatable_js.create_table(headers,rows)
        Dev.print(html)


