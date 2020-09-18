from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import json
from collections import OrderedDict
import re




class Product:
    def __init__(self, name, price, shop, link,img):
        self.name = name
        self.price = price
        self.shop = shop
        self.img = img
        self.link = link




class Chaldal:
    def __init__(self, search_key, area):
        headless_chrome = Options()
        headless_chrome.add_argument("--headless")
        self.driver = webdriver.Chrome('C:\\Users\\GK\\Desktop\\chromedriver.exe') #Change this to your ChromeDriver path.
        self.main_url = 'https://chaldal.com/search/'+search_key
        self.driver.get(self.main_url)
        self.search_str = search_key
        self.scroll_down()
        self.prod_list = self.getListofProducts()
        self.driver.close()





    def scroll_down(self):
        oldOffset = 0
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            offset = self.driver.execute_script("return document.documentElement.scrollTop - window.innerHeight;")
            if offset == oldOffset:
                break
            oldOffset = offset

            sleep(1)



    def select_area(self,area):
        try:
            state = Select(self.driver.find_element_by_id('state'))

            # select by visible text
            state.select_by_visible_text('Dhaka')

            city = Select(self.driver.find_element_by_id('city'))

            # select by visible text
            city.select_by_visible_text(area)

            setStoreBtn = self.driver.find_element_by_id('btnFindStore')

            setStoreBtn.click()

        except Exception:
            pass

    def getListofProducts(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        all_prods = soup.find_all('div', {'class': 'product'})

        p_list = []

        for x in all_prods:

            name = str(x.find('div',{'class': 'name'}))
            p = re.compile(r'<.*?>')
            name = p.sub('', name)
            if not re.search(self.search_str, name, re.IGNORECASE):
                continue
            price = str(x.find('div',{'class': 'price'}))
            price = p.sub('',price)
            pA = price.split(' ')
            price = pA[1]

            img = x.find('div',{'class': 'imageWrapperWrapper'}).find('img').get('src')
            link = "https://chaldal.com"+x.find('a',{'class': 'btnShowDetails'}).get('href')
            p = Product(name, price, 'Chaldal', link,img)
            p_list.append(p)


        return p_list


        #print(all_prods)




if __name__ == '__main__':
    app = Chaldal('butter','Uttara')
