from unittest                               import TestCase
from urllib.parse                           import urljoin
from osbot_utils.utils.Files                import file_contents, file_exists
from osbot_utils.utils.Misc                 import random_string
from osbot_browser.utils.Wait_For_Download  import Wait_For_Download
from osbot_browser.browser.Temp_Browser     import Temp_Browser
from osbot_utils.utils.Temp_File            import Temp_File
from osbot_utils.utils.Temp_Web_Server      import Temp_Web_Server


class test_Wait_For_Download(TestCase):

    def setUp(self) -> None:
        pass

    def test_get_file(self):
        headless = True
        file_size = 10                                  # goes up nicely to more that 1Mb
        random_text = random_string(length=file_size)
        with Temp_File(contents=random_text) as temp_file:
            root_folder      = temp_file.tmp_folder
            file_to_download = temp_file.tmp_file
            with Temp_Web_Server(root_folder=root_folder) as web_server:
                with Temp_Browser(headless=headless) as browser:
                    browser.set_auto_close(False)
                    browser.open(web_server.url())
                    full_link = urljoin(web_server.url(), file_to_download)

                    page      = browser.page()
                    wait_for_download = Wait_For_Download(page)
                    wait_for_download.sync_set_browser_download_folder()
                    wait_for_download.sync_trigger_download(full_link)

                    downloaded_file = wait_for_download.sync_get_file()
                    assert random_text == file_contents(downloaded_file)

    def test__enter__leave__(self):
        temp_file         = Temp_File        ()
        temp_web_server   = Temp_Web_Server  (root_folder=temp_file.tmp_folder)
        temp_browser      = Temp_Browser     (open_page=temp_web_server.url())
        full_link         = urljoin(temp_web_server.url(), temp_file.tmp_file)
        with temp_file:
            with temp_web_server:
                with temp_browser:
                    with Wait_For_Download(page=temp_browser.page()) as _:
                        _.sync_trigger_download(full_link)
                        _.sync_get_file()
                        assert _.status is True
                        assert file_exists(_.downloaded_file)



