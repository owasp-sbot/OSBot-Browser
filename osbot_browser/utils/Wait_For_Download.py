import asyncio

from syncer import sync

from osbot_utils.utils.Files import files_list, temp_folder


class Wait_For_Download:

    def __init__(self, page):
        self.page            = page
        self.target_folder   = temp_folder()
        self.downloaded_file = None
        self.target_url      = None
        self.status          = False

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
        files = await self.wait_for_files_in_folder()
        if files and len(files) == 1:                                   # there should only be one file in there
            self.downloaded_file = files[0]
            self.status = True
            return self.downloaded_file

    async def trigger_download(self, url, print_expected_error=False):
        try:
            await self.page.goto(url)
        except Exception as error:
            if print_expected_error:
                print(error)

    async def wait_for_files_in_folder(self, max_attempts=10, wait_for=0.5):
        for i in range(0, max_attempts):
            files = self.files_in_target_Folder()
            if len(files) > 0:
                return files
            await asyncio.sleep(wait_for)
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