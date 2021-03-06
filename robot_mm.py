import json5
import re
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

import pandas as pd

class Robot_mm:

    def __init__(self):
        '''
        inicjacja danych o sklepie dla bota
        '''
        self.url_media_beg = "https://mediamarkt.pl/rtv-i-telewizory/telewizory?page="
        self.url_media_base = "https://mediamarkt.pl"

        # Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25
        # Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5

        ua = UserAgent()

        self.header = {'User-Agent': str(ua.safari)}

    def GetPagesCount(self) -> int:
        '''
        Szuka na stronie liczby stron
        :return: Zwraca liczbę strony z ofertami
        '''
        self._Connect_wPage(1)
        page_soup = self.soup_mm.find("span", {"class" : "m-pagination_count"})
        pages_num = int(str(page_soup.text).replace("z", ""))
        return pages_num

    def _Connect_wPage(self, page_num) -> bool:
        '''
        Ustanawia połączenie z wybraną stroną z ofertami
        :param page_num: numer strony z którą nawiązywane jest połączenie
        :return: zwraca True, jeśli operacja nawiązania połączenia się powiedzie
        '''
        try:
            self.respond_mm = requests.get(self.url_media_beg + str(page_num), headers=self.header)
            self.soup_mm = bs(self.respond_mm.content, 'html.parser')
            return True
        except:
            return False

    def _GetProductData(self, link):
        '''
        Zbiera informacje o konkretnym produkcie
        :param link: link do danego produktu
        :return: [] !!!!
        '''
        try:
            new_resp = requests.get(url=link, headers = self.header)
            soup = bs(new_resp.content, 'html.parser')
            param_tables = soup.find("div", {"class" : "m-offerShowData"})
            param_table = param_tables.find_all("div", {"class" : "m-offerShowData_item js-offerShowData_item js-offerShowData"})
            featuresTech = param_table[0].find_all("span")
            featuresScr = param_table[1].find_all("span")
            featuresBrand = param_table[8].find_all("a")

            matrixType = str(featuresTech[1].text)
            smartTV = str(featuresTech[3].text)
            size = str(featuresScr[1].text)
            resolution = str(featuresScr[9].text)
            resolutionName = str(featuresScr[7].text)
            brand = str(featuresBrand[0].text)
            title = soup.find("h1", {"class" : "b-ofr_headDataTitle"})
            name = str(title.text).replace("Telewizor ", "")

            param_price_box = soup.find("div", {"class" : "b-contentSideBox"})
            param_price = param_price_box.find("div", {"class" : "m-priceBox_price"})
            price = str(param_price.text).replace(" ", "").replace(",-zł","").replace("\n", "")

            return brand, name, price, size, resolution, resolutionName, matrixType, smartTV
        except:
            return [0, 0, 0, 0, 0, 0, 0, 0]

    def _CollectDataFromPage(self, num):
        '''
        Zbiera informacje o grupie produktów z danej strony
        :param num: numer strony
        :return: lista produktów ze strony
        '''
        list = []
        product_list = self.soup_mm("div", {"class": "b-row clearfix2 b-listing_classic js-eqContainer js-offerBox js-equalHRow"})
        product = product_list[0].find_all("div", {"class": "m-offerBox_content"})

        for p in product:
            name_scr = p.find("div", {"class": "m-offerBox_box"})
            name_a = name_scr.find("a")
            link = self.url_media_base + name_a.get('href')
            brand, name, price, size, resolution, resolutionName, matrixType, smartTV = self._GetProductData(link)
            list += [[brand, name, price, size, resolution, resolutionName, matrixType, smartTV]]
        return list

    def CollectData_mm(self, pages=-1):
        '''
        Metoda główna bota : Zbiera informacje za pomocą pozostałych funkcji
        :param pages: numer strony do której ma pracować, standarodwo '-1', wtedy pobiera całkowitą liczbę stron
        :return: zwraca listę
        '''
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
    # testy
    rb = Robot_mm()
    x = rb.GetPagesCount()
    print(x)
    list = rb.CollectData_mm(2)
    print(len(list))
    print(list)

    data = pd.DataFrame(list)
    print(data)
    print(data.shape)