from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas
from view_helpers.DataTable_Js import DataTable_Js
from view_helpers.Google_Charts_Js import Google_Charts_Js
from view_helpers.Vis_Js_Views import Vis_Js_Views


class Test_Google_Charts_Js(TestCase):

    def setUp(self):
        self.png_data   = None
        self.google_charts = Google_Charts_Js()

    # def tearDown(self):
    #     if self.png_data:
    #         Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_load_page(self):
        self.google_charts.load_page(True)

    def test_create_data_table(self):
        self.google_charts.create_data_table()
