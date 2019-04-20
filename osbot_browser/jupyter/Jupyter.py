from time import sleep

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_browser.browser.API_Browser import API_Browser


class Jupyter:

    def __init__(self, pwd_token):
        self.browser        = API_Browser(headless=False)
        self.server         = {'schema':'http', 'ip':  '127.0.0.1' , 'port' : 8888 }
        self.pwd_token      = pwd_token
        self.tmp_screenshot = '/tmp/jupyter_screenshot.png'

    def browser_width(self,width):
        self.browser.sync__browser_width(width=width)
        return self

    def current_page(self):
        return self.browser.sync__url()

    def login(self):
        return self.open('?token={0}'.format(self.pwd_token))

    def logout(self):
        return self.open('logout')

    def open(self, path):
        url = self.resolve_url(path)
        self.browser.sync__open(url)
        return self

    def open_notebook(self,notebook_path):
        return self.open('nbconvert/html/{0}.ipynb?download=false'.format(notebook_path))

    def open_notebook_edit(self, notebook_path):
        return self.open('notebooks/{0}.ipynb'.format(notebook_path))

    def open_tree(self):
        return self.open('tree')

    def screenshot(self):
        self.browser.sync__screenshot(full_page=True, file_screenshot=self.tmp_screenshot)
        return self.tmp_screenshot

    def resolve_url(self,path=None):
        if   path is None or len(path) == 0: path = '/'
        elif path[0] != '/'                : path = '/' + path

        return "{0}://{1}:{2}{3}".format(self.server.get('schema'), self.server.get('ip'),self.server.get('port'),path)

    def ui_hide_input_boxes(self):
        self.browser.sync__js_execute("$('div.input').hide()")
        return self