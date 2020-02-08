from unittest import TestCase

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Google_Charts_Js import Google_Charts_Js


class Test_Google_Charts_Js(Test_Helper):

    def setUp(self):
        super().setUp()
        self.headless   = False
        self.png_data   = None
        self.google_charts = Google_Charts_Js(headless=self.headless)

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_load_page(self):
        self.google_charts.load_page(True)

    def test_create_data_table(self):
        self.google_charts.load_page(True)
        options = {'title':'an Chart',
                   'curveType': 'function',
                   'legend': {'position': 'bottom'},
                   'width': 800,
                   'height':500
                   };
        data = [['Year', 'Sales', 'Expenses'],
                ['2004', 1000, 400],
                ['2005', 1170, 460],
                ['2006', 660, 1120],
                ['2007', 1030, 540]]
        self.png_data = self.google_charts.create_data_table(options, data)
