"""
MM ma zabezpieczenia przeciw botom
euro działa

pobieram :
        * producent
        * model
        * wielkość
        * rozdzielczość
        * smartTV
        1 id
        2 name
        3 brand
        7 price
        8 link
"""
import json5
import re
import requests
from bs4 import BeautifulSoup as bs

import pandas as pd


class Robot_euro:

    def __init__(self):
        self.url_euro_tv_beg = 'https://www.euro.com.pl/telewizory-led-lcd-plazmowe,strona-'
        self.url_euro_tv_end = '.bhtml'
        self.url_euro_base = 'https://www.euro.com.pl'
        self.licznik_niedostepnych = 0

    def GetPagesCount(self) -> int:
        page_soup = self.soup_euro.find("div", { "class" : "paging-numbers"})
        page_list = page_soup.find_all("a")
        last_page = len(page_list) - 1
        return int(page_list[last_page].text)

    def _Connect_wPage(self, page_num) -> bool:
        try:
            self.respond_euro = requests.get(self.url_euro_tv_beg + str(page_num) + self.url_euro_tv_end)
            self.soup_euro = bs(self.respond_euro.content, 'html.parser')
            return True
        except:
            return False

    def _GetProductData(self, soup):
        param_table = soup.find("table", {"class": "description-tech-details js-tech-details"})

        params = param_table.find_all("td")

        s_size = params[3].text.replace("\t", "").replace("\n", "")
        resolution = params[5].text.replace("\t", "").replace("\n", "")
        matrixType = params[11].text.replace("\t", "").replace("\n", "")
        smartTV = params[39].text.replace("\t", "").replace("\n", "")
        return s_size, resolution, matrixType, smartTV

    def _CollectDataFromPage(self, num):
        list = []
        if self._Connect_wPage(num) == True:
            product_list = self.soup_euro.find("div", {"id": "product-list"})
            product_script = product_list.find_all("script", {"type": "text/javascript"})

            norm = str(product_script).replace("\t", "").replace("\n", "")
            data = re.search(r'\((.*?)\)', norm)

            js_script = json5.loads(data.group(1))
            js_prod = json5.loads(js_script['products'])
            for tv in js_prod:
                js = json5.loads(tv)
                brand = js['brand']
                name = js['name']
                price = js['price']
                id = js['id']

                link = js['link']
                try:
                    new_resp = requests.get(url=self.url_euro_base + link)
                    soup = bs(new_resp.content, 'html.parser')
                    s_size, resolution, matrixType, smartTV = self._GetProductData(soup)
                    list.append([brand, name, price, id, s_size, resolution, matrixType, smartTV])
                except:
                    self.licznik_niedostepnych += 1
        else:
            self.licznik_niedostepnych += 1

        return list

    def CollectData_euro(self, pages=-1):
        list = []
        if self._Connect_wPage(1) == False:
            return list
        if pages == -1:
            pages_num = self.GetPagesCount()
        else:
            max = self.GetPagesCount()
            if pages + 1 <= max:
                pages_num = pages + 1
            else:
                pages_num = max

        for num in range(1, pages_num):
            print(num)
            list += self._CollectDataFromPage(num)

        return list


if __name__ == '__main__':
    rb = Robot_euro()
    list = rb.CollectData_euro()
    print(len(list))
    print(list)

    data = pd.DataFrame(list)
    print(data)
    print(data.shape)

