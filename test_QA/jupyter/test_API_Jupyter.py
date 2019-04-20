from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.jupyter.API_Jupyter import API_Jupyter


class test_API_Jupyter(TestCase):

    def setUp(self):
        self.pwd_token = '....'
        self.api       = API_Jupyter(pwd_token=self.pwd_token)

    def test__init__(self):
        assert type(self.api).__name__ == 'API_Jupyter'
        assert self.api.server         == {'schema':'http', 'ip':  '127.0.0.1' , 'port' : 8888 }

    def test_login(self):
        result = self.api.login()
        Dev.pprint(result)

    def test_open_notebook(self):
        self.api.open_notebook('work/test-notebook')

    def test_open_notebook_edit(self):
        self.api.open_notebook_edit('work/test-notebook')

    def test_open_tree(self):
        result = self.api.open_tree()
        Dev.pprint(result)

    def test_screenshot(self):
        #target  = 'work/with-slider'
        target = 'work/test-notebook'
        (
            self.api.open_notebook(target)
                    .ui_hide_input_boxes()
                    .browser_width(1200)
                    .screenshot()
        )
        Dev.pprint(self.api.tmp_screenshot)

    def test_resolve_url(self):
        assert self.api.resolve_url('/aaa') == 'http://127.0.0.1:8888/aaa'
        assert self.api.resolve_url('/a/b') == 'http://127.0.0.1:8888/a/b'
        assert self.api.resolve_url('aaaa') == 'http://127.0.0.1:8888/aaaa'
        assert self.api.resolve_url('a/bb') == 'http://127.0.0.1:8888/a/bb'
        assert self.api.resolve_url(''    ) == 'http://127.0.0.1:8888/'
        assert self.api.resolve_url(      ) == 'http://127.0.0.1:8888/'
        assert self.api.resolve_url(None  ) == 'http://127.0.0.1:8888/'