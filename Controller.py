"""
klasa pozwalająca kontrolować klasy botów
"""

import pandas as pd

from robot_mm import Robot_mm
from robot_euro import Robot_euro

class Controller:
    def __init__(self):
        self.list_mm = []
        self.list_euro = []
        self._shops = {'euro' : 5,
                       'mm' : 10,
                       'all' : 15
                       }
        self.rb_mm = Robot_mm()
        self.rb_euro = Robot_euro()

    def GetList(self, key: str = 'all', pages: int = 0):
        '''
            Funkcja przeszukuje strony sklepów i tworzy listęproduktów
        :param key: klucz z biblioteki _shops jej zakres pozwala wybrać sklap w celu poszukiwań {'euro', 'mm', 'all'}
        :param pages: liczba stron przeszukiwanych
        :return: zwraca listę
        '''
        if self._shops[key] != 5:
            if pages == 0:
                self.list_mm = self.rb_mm.CollectData_mm()
            else:
                self.list_mm = self.rb_mm.CollectData_mm(pages)
        if self._shops[key] != 10:
            if pages == 0:
                self.list_euro = self.rb_euro.CollectData_euro()
            else:
                self.list_euro = self.rb_euro.CollectData_euro(pages)

        list= self.list_mm + self.list_euro
        return list



    def MakeExcelFrom_mm(self):
        '''
        Tworzy plik Excel na podstawie znalezionych produktów w MM
        :return:
        '''
        if not self.list_mm:
            self.GetList('mm')
            data = pd.DataFrame(self.list_mm)
        else:
            data = pd.DataFrame(self.list_mm)
        data.to_excel("out_mm.xlsx", sheet_name="sh1")

    def MakeExcelFrom_euro(self):
        '''
        Tworzy plik Excel na podstawie znalezionych produktów w Euro
        :return:
        '''
        if not self.list_euro:
            self.GetList('euro')
            data = pd.DataFrame(self.list_euro)
        else:
            data = pd.DataFrame(self.list_euro)
        data.to_excel("out_euro.xlsx", sheet_name="sh1")

    def MakeExcel(self):
        '''
        Tworzy jeden wspólny Excel
        :return:
        '''
        if not self.list_mm:
            self.GetList('mm')
        if not self.list_euro:
            self.GetList('euro')
        data = pd.DataFrame(self.list_mm + self.list_euro)
        data.to_excel("out.xlsx", sheet_name="sh1")

        data.to_excel("out.xlsx", sheet_name="sh1")

    # data = pd.DataFrame(list, columns=['brand', 'name', 'price', 'id', 'size', 'resolution', 'matrix type', 'smartTV'])

if __name__ == '__main__':
    ctrl = Controller()
    listmm = ctrl.GetList('mm', 2)
    print(listmm)
    print(len(listmm))
    listeu = ctrl.GetList('euro', 2)
    print(listeu)
    print(len(listeu))
    list = ctrl.GetList(pages=2)
    print(list)
    print(len(list))

