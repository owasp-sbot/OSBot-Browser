from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from osbot_browser.jupyter.Jupyter import Jupyter


class test_Jupyter(TestCase):

    def setUp(self):
        self.pwd_token = '0a849b6edb98721f0cab1dc7ac5234fe655e018d009d98b8'
        self.jp   = Jupyter(pwd_token=self.pwd_token)

    def test__init__(self):
        assert type(self.jp).__name__ == 'Jupyter'
        assert self.jp.server == {'schema': 'http', 'ip': '127.0.0.1' , 'port' : 8888}

    def test_login(self):
        self.jp.logout()                                                            # log out user
        assert self.jp.current_page() == 'http://127.0.0.1:8888/logout'             # confirm we are in logout page
        self.jp.open_tree()                                                         # try to open tree page
        assert self.jp.current_page() == 'http://127.0.0.1:8888/login?next=%2Ftree' # confirm redirect to login
        self.jp.login()                                                             # log in user
        assert self.jp.current_page() == 'http://127.0.0.1:8888/tree'               # confirm now on tree page

    def test_open_notebook(self):
        notebook_path = 'work/test-notebook'
        self.jp.open_notebook(notebook_path)
        assert self.jp.current_page() == 'http://127.0.0.1:8888/nbconvert/html/{0}.ipynb?download=false'.format(notebook_path)

    def test_open_notebook_edit(self):
        self.jp.open_notebook_edit('work/test-notebook')
        assert self.jp.current_page() == 'http://127.0.0.1:8888/notebooks/work/test-notebook.ipynb'

    def test_open_tree(self):
        assert self.jp.open_tree().current_page() == 'http://127.0.0.1:8888/tree'

    def test_screenshot(self):
        #target  = 'work/with-slider'
        target = 'work/test-notebook'
        (
            self.jp.open_notebook(target)
                    .ui_hide_input_boxes()
                    .browser_width(1200)
                    .screenshot()
        )
        assert Files.exists(self.jp.tmp_screenshot)

    def test_resolve_url(self):
        assert self.jp.resolve_url('/aaa') == 'http://127.0.0.1:8888/aaa'
        assert self.jp.resolve_url('/a/b') == 'http://127.0.0.1:8888/a/b'
        assert self.jp.resolve_url('aaaa') == 'http://127.0.0.1:8888/aaaa'
        assert self.jp.resolve_url('a/bb') == 'http://127.0.0.1:8888/a/bb'
        assert self.jp.resolve_url(''    ) == 'http://127.0.0.1:8888/'
        assert self.jp.resolve_url(      ) == 'http://127.0.0.1:8888/'
        assert self.jp.resolve_url(None  ) == 'http://127.0.0.1:8888/'