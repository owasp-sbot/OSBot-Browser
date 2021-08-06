from unittest import TestCase

from osbot_browser.javascript.Javascript_Parser import js_parser_from_url
from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint
from syncer import sync

from osbot_browser.browser.Temp_Browser import Temp_Browser


class test_Temp_Browser(TestCase):

    # todo: Javascript below shows 2 missing types : LabeledStatement , ContinueStatement
    def test__enter__exit__(self):
        headless = True
        with Temp_Browser(headless=headless) as browser:
            browser.open('https://www.google.com')
            assert browser.api_browser.sync__url() == 'https://www.google.com/'

            raw_html = browser.html()
            py_query = browser.py_query()
            assert "<title>Google</title>" in raw_html
            assert py_query.query('title').text() == 'Google'
            assert py_query.query('form').attributes() == {'action': '/search', 'method': 'GET', 'role': 'search'}
            scripts_urls = list_set(py_query.query('script').indexed_by_attribute('src'))
            first_script = scripts_urls[0]
            js_parser = js_parser_from_url(first_script)

            assert len(js_parser.var_names       ()) > 300
            assert len(js_parser.function_names  ()) > 10
            assert len(js_parser.identifier_names()) > 1000
            literals_with_https = js_parser.literal_names       (min_name_size=5, starts_with='"https://')
            assert literals_with_https == [    '"https://accounts.google.com/o/oauth2/auth"',
                                              '"https://accounts.google.com/o/oauth2/postmessageRelay"',
                                              '"https://apis.google.com"',
                                              '"https://clients6.google.com"',
                                              '"https://content.googleapis.com"',
                                              '"https://domains.google.com/suggest/flow"',
                                              '"https://plus.google.com"',
                                              '"https://plus.googleapis.com"',
                                              '"https://workspace.google.com/:session_prefix:marketplace/appfinder?usegapi=1"',
                                              '"https://www.googleapis.com/auth/plus.me"',
                                              '"https://www.googleapis.com/auth/plus.people.recommended"']






