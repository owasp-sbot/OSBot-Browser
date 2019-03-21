from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from view_helpers.Full_Calendar_Views import Full_Calendar_Views


class Test_Full_Calendar_Views(TestCase):

    def setUp(self):
        self.calendar_views = Full_Calendar_Views()

    def tearDown(self):
        Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_default(self):
        self.png_data = self.calendar_views.default(headless=True)
        Dev.pprint(self.png_data)
