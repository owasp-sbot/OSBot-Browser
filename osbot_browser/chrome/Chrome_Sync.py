from syncer import sync

from osbot_browser.chrome.Chrome import Chrome


class Chrome_Sync:
    def __init__(self, chrome: Chrome =None):
        self.chrome = chrome or Chrome()

    def api_browser(self):      # todo: figure out if this is the best way to expose this object
        from osbot_browser.browser.API_Browser import API_Browser
        return API_Browser(self.browser())

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