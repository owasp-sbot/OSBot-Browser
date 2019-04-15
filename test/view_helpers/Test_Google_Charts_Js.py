from unittest import TestCase

from osbot_browser.view_helpers.Google_Charts_Js import Google_Charts_Js


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
