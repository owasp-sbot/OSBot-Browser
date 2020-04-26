from osbot_browser.chrome.Chrome import Chrome
from osbot_utils.decorators.Sync import sync


class Chrome_Sync:
    def __init__(self):
        self.chrome = Chrome()

    @sync
    async def browser(self):
        return await self.chrome.browser()

    @sync
    async def close(self):
        return await self.chrome.close()

    @sync
    async def open(self, url):
        await (await self.chrome.page()).goto(url)
        return self

    @sync
    async def url(self):
        return (await self.chrome.page()).url

    @sync
    async def screenshot(self):
        return await (await self.chrome.page()).screenshot()


    # browser wrapper helper methods

    def keep_open(self):
        self.chrome.keep_open()
        return self