from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files


class View_Examples:

    def __init__(self):
        self.render_page = Render_Page(headless = False, auto_close = False)
        self.path_views  = Files.path_combine('.','../../views')

    def hello_world(self):
        file = self.path_views + '/examples/hello-world.html'
        Dev.print(Files.contents(file))
        return self.render_page.render_html("<h1>test</h1>")

