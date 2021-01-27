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

    def GetList(self, key: str = 'all'):
        if self._shops[key] != 5:
            self.list_mm = self.rb_mm.CollectData_mm()
        if self._shops[key] != 10:
            self.list_euro = self.rb_euro.CollectData_euro()

        list= self.list_mm + self.list_euro
        return list



    def MakeExcelFrom_mm(self):
        if not self.list_mm:
            self.GetList('mm')
            data = pd.DataFrame(self.list_mm)
        else:
            data = pd.DataFrame(self.list_mm)
        data.to_excel("out_mm.xlsx", sheet_name="sh1")

    def MakeExcelFrom_euro(self):
        if not self.list_euro:
            self.GetList('euro')
            data = pd.DataFrame(self.list_euro)
        else:
            data = pd.DataFrame(self.list_euro)
        data.to_excel("out_euro.xlsx", sheet_name="sh1")

    def MakeExcel(self):
        if not self.list_mm:
            self.GetList('mm')
        if not self.list_euro:
            self.GetList('euro')
        data = pd.DataFrame(self.list_mm + self.list_euro)
        data.to_excel("out.xlsx", sheet_name="sh1")

        data.to_excel("out.xlsx", sheet_name="sh1")

    # data = pd.DataFrame(list, columns=['brand', 'name', 'price', 'id', 'size', 'resolution', 'matrix type', 'smartTV'])
