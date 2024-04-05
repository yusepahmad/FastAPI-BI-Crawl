from .helper import Helper
from playwright.async_api import async_playwright

class HardCode(Helper):
    def __init__(self):
        super().__init__()
        self.playwright = None
        self.browser = None
        self.page = None

    async def init_playwright(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def close(self):
        await self.page.close()
        await self.browser.close()
        await self.playwright.stop()

    async def kurs(self, option, akses, start, end):
        await self.init_playwright()
        if end is None and akses == "Time Series":
            await self.close()
            return "please choose end date"
        await self.page.goto('https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/default.aspx')
        await self.choose_uang(self.page, option)
        await self.choose_akses(self.page, akses)
        await self.choose_date_year(self.page, akses, start, end)
        result = await self.tbody_kurs(self.page, start, akses, option)
        await self.close()
        return result

    async def dana_inflasi(self, start, end):
        await self.init_playwright()
        await self.page.goto('https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx')
        if start:
            await self.date_page_inf(self.page, start, end)
        result = await self.tbody(self.page)
        await self.close()
        return result

    async def data_suku(self, start, end):
        await self.init_playwright()
        await self.page.goto('https://www.bi.go.id/id/statistik/indikator/bi-rate.aspx')
        if start:
            await self.date_page(self.page, start, end)
        result = await self.tbody_suku(self.page)
        await self.close()
        return result
