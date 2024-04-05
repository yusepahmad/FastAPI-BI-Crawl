from ..core.s3 import S3

class Helper(S3):
    def __init__(self):
        super().__init__()



    async def choose_date_year(self, page, akses, start, end=None):
        async def choose_date_1(page, value, choose):
            await page.evaluate(f'''(value, choose) => {{
                const xpath = "//html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div[1]/div/div/div[3]/div[{choose}]/div/div/input";
                const input = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (input) {{
                    input.value = '{value}';
                }}
            }}''')

        async def choose_date_2(page, value):
            await page.evaluate(f'''(value, choose) => {{
                const xpath = "//html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[1]/div/div/input";
                const input = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (input) {{
                    input.value = '{value}';
                }}
            }}''')

        if akses == "Time Series":
            await choose_date_1(page, str(start), 1)
            await choose_date_1(page, str(end), 2)
            await page.click('//html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div[1]/div/div/div[3]/div[3]/input')
        else:
            await choose_date_2(page, str(start))
            await page.click('//html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div[1]/div/div/div[2]/div[2]/input')

    async def choose_akses(self, page, akses):
        select_selector = '//*[@id="selectPeriod"]'
        await page.select_option(select_selector, value=akses)

    async def choose_uang(self, page, option_value):
        select_selector = '#ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_ddlmatauang1'
        await page.select_option(select_selector, value=option_value)

    async def option(self, page):
        select = await page.query_selector('//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_MataUang"]/div[2]/div/div')
        for option in await select.query_selector_all('option'):
            print(await option.inner_text())

    async def choose_date(self, page, value, choose):
        await page.evaluate(f'''(value, choose) => {{
            const xpath = "//html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div[{choose}]/div/div/input[1]";
            const input = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (input) {{
                input.value = '{value}';
            }}
        }}''')

    async def date_page(self, page, start, end):
        await self.choose_date(page, str(start), 1)
        await self.choose_date(page, str(end), 2)
        await page.click('//*[@id="ctl00_ctl54_g_78f62327_0ad4_4bb8_b958_a315eccecc27_ctl00_ButtonSearch"]')

    async def date_page_inf(self, page, start, end):
        await self.choose_date(page, str(start), 1)
        await self.choose_date(page, str(end), 2)
        await page.click('//*[@id="ctl00_ctl54_g_1f0a867d_90e9_4a92_b1c8_de34738fc4f1_ctl00_ButtonCari"]')

    async def tbody(self, page):
        datas = []
        while True:
            try:
                await page.wait_for_selector('.next', timeout=3000)
                await page.wait_for_selector('table')
                tbody = await page.query_selector('table')
                data = await self.data_table(tbody)
                datas.extend(data)
                await page.click('input.next')
            except:
                await page.wait_for_selector('table')
                tbody = await page.query_selector('table')
                data = await self.data_table(tbody)
                datas.extend(data)
                break
        return datas

    async def data_table(self, tbody):
        data_table = []
        for tr in await tbody.query_selector_all('tr'):
            row = []
            for td in await tr.query_selector_all('td'):
                text = await td.inner_text()
                row.append(text)
            if row:
                data_table.append({'date': row[0], 'inflation': row[1]})
        return data_table

    async def tbody_suku(self, page):
        datas = []
        while True:
            try:
                await page.wait_for_selector('.next', timeout=1500)
                await page.wait_for_selector('table')
                tbody = await page.query_selector('table')
                data = await self.data_table_suku(tbody)
                datas.extend(data)
                await page.click('input.next')
            except:
                await page.wait_for_selector('table')
                tbody = await page.query_selector('table')
                data = await self.data_table_suku(tbody)
                datas.extend(data)
                break
        return datas

    async def data_table_suku(self, tbody):
        data_table = []
        for tr in await tbody.query_selector_all('tr'):
            row = []
            for td in await tr.query_selector_all('td'):
                text = await td.inner_text()
                row.append(text)
            if row:
                data_table.append({'date': row[0], 'bi_rate': row[1], 'link': row[2]})
        return data_table

    async def tbody_kurs(self, page, start, akses, option):
        datas = []
        await page.wait_for_selector('table')
        tbody = await page.query_selector('table')
        data = await self.data_table_kurs(tbody, akses, option, start)
        datas.extend(data)
        return datas

    async def data_table_kurs(self, tbody, akses, option, start):
        data_table = []
        for tr in await tbody.query_selector_all('tr'):
            row = []
            for td in await tr.query_selector_all('td'):
                text = await td.inner_text()
                row.append(text)
            if row:
                if akses == "Time Series":
                    data_table.append({
                        'Mata Uang': option,
                        'Nilai': row[0],
                        'Kurs Jual': row[1],
                        'Kurs Beli': row[2],
                        'tanggal': row[3]
                    })
                elif akses == "Harian":
                    data_table.append({
                        'Mata Uang': row[0],
                        'Nilai': row[1],
                        'Kurs Jual': row[2],
                        'Kurs Beli': row[3],
                        'tanggal': start
                    })
        return data_table
