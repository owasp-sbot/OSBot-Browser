import asyncio

from osbot_utils.utils.Misc import bytes_to_base64
from syncer import sync

from osbot_utils.utils.Files import files_list, temp_folder


class Wait_For_Download:

    def __init__(self, page, capture_screenshots=False, max_attempts=20, wait_for=0.5):
        self.page                = page
        self.capture_screenshots = capture_screenshots
        self.target_folder       = temp_folder()
        self.downloaded_file     = None
        self.target_url          = None
        self.screenshots         = []
        self.status              = False
        self.max_attempts        = max_attempts
        self.wait_for            = wait_for
        self.wait_count          = 0
        self.waited_for          = 0

    def __enter__(self):
        self.sync_set_browser_download_folder()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def set_browser_download_folder(self):
        cdp = await self.page.target.createCDPSession()
        await cdp.send( "Page.setDownloadBehavior",
                        {"behavior": "allow", "downloadPath": self.target_folder})

    def files_in_target_Folder(self):
        return files_list(self.target_folder)

    async def get_file(self):
        files           = await self.wait_for_files_in_folder()
        self.waited_for = self.wait_count * self.wait_for
        if files and len(files) == 1:                                   # there should only be one file in there
            self.downloaded_file = files[0]
            self.status          = True
            return self.downloaded_file

    async def capture_screenshot(self):
        if self.capture_screenshots:
            full_page         = True
            screenshot_bytes  = await self.page.screenshot({'fullPage': full_page})
            screenshot_base64 = bytes_to_base64(screenshot_bytes)
            self.screenshots.append(screenshot_base64)

    async def trigger_download(self, url, print_expected_error=False):
        try:
            await self.page.goto(url)
        except Exception as error:
            if print_expected_error:
                print(error)

    async def wait_for_files_in_folder(self):
        for self.wait_count in range(1, self.max_attempts + 1):
            files = self.files_in_target_Folder()
            if len(files) > 0:
                return files
            await self.capture_screenshot()
            await asyncio.sleep(self.wait_for)
        return None

    @sync
    async def sync_get_file(self):
        return await self.get_file()

    @sync
    async def sync_set_browser_download_folder(self):
        return await self.set_browser_download_folder()

    @sync
    async def sync_trigger_download(self, url):
        return await self.trigger_download(url)