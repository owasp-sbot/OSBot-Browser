import os
from unittest import TestCase

from browser.Render_Page import Render_Page
from src.view_helpers.View_Examples import View_Examples
from utils.Dev import Dev
from utils.Misc import Misc


class Test_Render_Page(TestCase):
    def setUp(self):
        self.render_page = View_Examples('/tmp/test_screenshot_html.png')

    def test_hello_world(self):
        result = self.render_page.hello_world__html()
        assert '<h1>Hello World.....</h1>' in result.html()

    def test_hello_world(self):

        self.render_page.clip = {'x': 1, 'y': 1, 'width': 220, 'height': 50}
        self.render_page.hello_world()

    def test_bootstrap_cdn(self):
        self.render_page.bootstrap_cdn()

    def test_zipped_views(self):
        zip_file = self.render_page.zipped_views()
        Dev.pprint(zip_file)
        os.remove(zip_file)