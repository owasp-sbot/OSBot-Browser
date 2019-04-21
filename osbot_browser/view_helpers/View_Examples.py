from browser import Render_Page
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Unzip_File import Unzip_File
from pbx_gs_python_utils.utils.Zip_Folder import Zip_Folder


class View_Examples:

    def __init__(self,tmp_img=None, clip=None, headless=False):
        self.headless    = headless
        self.path_views  = Files.path_combine(Files.parent_folder(__file__),'../../osbot_browser/web_root')
        self.render_page = Render_Page(headless=self.headless, web_root=self.path_views)
        self.tmp_img     = tmp_img
        self.clip        = clip

    def _open_file_and_get_html(self, filename):
        file = '{0}{1}{2}'.format(self.path_views, '/examples/',filename)
        return self.render_page.render_file(file)

    def _open_file_and_take_screenshot(self, filename):
        file = '{0}{1}{2}'.format(self.path_views, '/examples/',filename)
        return self.render_page.screenshot_file(file, self.tmp_img, self.clip)

    def set_clip (self, clip):
        self.clip = clip
        return self

    def render_file_from_zip(self, target):
        with Zip_Folder(self.path_views) as zip_file:
            with Unzip_File(zip_file,'/tmp/test_render_from_zip', True) as web_root:
                return self.render_page.screenshot_file_in_folder(web_root, target, self.tmp_img)

    def open_file_in_browser(self, path,js_code=None):
        with self.render_page.web_server as web_server:
            url = web_server.url(path)
            return self.render_page.get_page_html_via_browser(url,js_code)

    # def open_file_in_browser_and_invoke_js(self, path, js_to_invoke):
    #     with self.render_page.web_server as web_server:
    #         url = web_server.url(path)
    #         return self.render_page.get_page_html_via_browser(url)


    def hello_world__html(self): return self._open_file_and_get_html        ('hello-world.html')
    def hello_world      (self): return self._open_file_and_take_screenshot ('hello-world.html')
    def bootstrap_cdn    (self): return self._open_file_and_take_screenshot ('bootstrap-cdn.html')
    def bootstrap_local  (self): return self.render_file_from_zip           ('/examples/bootstrap-local.html')
    def folder_root      (self): return self.render_page.screenshot_folder  (self.path_views, self.tmp_img)

    #self.render_page.screenshot_file_in_folder(web_root, target, self.tmp_img)


    #def zipped_views(self):
    #    return Files.zip_folder(self.path_views)