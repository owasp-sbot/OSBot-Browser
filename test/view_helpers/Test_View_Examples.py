from unittest import TestCase

from browser.Render_Page import Render_Page
from src.view_helpers.View_Examples import View_Examples
from utils.Dev import Dev
from utils.Misc import Misc


class Test_Render_Page(TestCase):
    def setUp(self):
        self.render_page = View_Examples()

    def test_hello_world(self):
        result = self.render_page.hello_world()
        Dev.pprint(result.html())
