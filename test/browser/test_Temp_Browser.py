from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from syncer import sync

from osbot_browser.browser.Temp_Browser import Temp_Browser


class test_Temp_Browser(TestCase):

    def test__enter__exit__(self):
        with Temp_Browser() as browser:
            browser.open('https://www.google.com')
            pprint(browser.html())

