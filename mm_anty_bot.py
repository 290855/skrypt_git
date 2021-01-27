"""
klasa prezentująca działanie zabezpieczeń anty botowych serwisu MediaMarkt
"""

from bs4 import BeautifulSoup
import requests

class Robot_wyklety:
    def __init__(self):
        self.url_media = "https://mediamarkt.pl/rtv-i-telewizory/telewizory?page=1"
        try:
            self.respond = requests.get(self.url_media)
        except:
            print("brak połączenia")

    def Connect(self):
        soup = BeautifulSoup(self.respond.content, 'html.parser')
        return soup

    def Get_html(self):
        soup = self.Connect()
        return str(soup.text)

if __name__ == '__main__':
    rb = Robot_wyklety()
    warn = rb.Get_html()
    print(warn)