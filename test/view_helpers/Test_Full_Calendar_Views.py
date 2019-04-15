from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda

from browser import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Full_Calendar_Views import Full_Calendar_Views


class Test_Full_Calendar_Views(TestCase):

    def setUp(self):
        self.calendar_views = Full_Calendar_Views()
        self.png_data       = None

    def tearDown(self):
        Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_default(self):
        self.png_data = self.calendar_views.gs_team(headless=False)
        self.png_data = self.png_data


    def test_default__via_lambda(self):
        self.lambda_browser = Lambda('browser.lambda_browser')
        self.lambda_browser.update_with_src()
        payload = {"params": ['calendar','gs_team'],'data': {'team_id':'T7F3AUXGV', 'channel':'DDKUZTK6X'}}
        self.lambda_browser.invoke(payload)