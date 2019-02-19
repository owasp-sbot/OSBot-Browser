from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files


class View_Examples:

    def __init__(self,tmp_img=None, clip=None):
        self.render_page = Render_Page()
        self.path_views  = Files.path_combine('.','../../views')
        self.tmp_img     = tmp_img
        self.clip        = clip

    def _open_file_and_get_html(self, filename):
        file = '{0}{1}{2}'.format(self.path_views, '/examples/',filename)
        return self.render_page.render_file(file)

    def _open_file_and_take_screenshot(self, filename):
        file = '{0}{1}{2}'.format(self.path_views, '/examples/',filename)
        return self.render_page.screenshot_file(file, self.tmp_img, self.clip)

    def hello_world__html(self): return self._open_file_and_get_html('hello-world.html')

    def hello_world      (self): return self._open_file_and_take_screenshot('hello-world.html')
    def bootstrap_cdn    (self): return self._open_file_and_take_screenshot('bootstrap-cdn.html')

    def zipped_views(self):
        return Files.zip_folder(self.path_views)