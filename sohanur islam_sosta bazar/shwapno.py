from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import json
import re



class Product:
    def __init__(self, name, price, shop, link, img):
        self.name = name
        self.price = price
        self.shop = shop
        self.img = img
        self.link = link




class Shwapno:
    def __init__(self, search_key, area):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome('C:\\Users\\GK\\Desktop\\chromedriver.exe') #Change this to your ChromeDriver path.
        self.search_str = search_key
        self.main_url = 'https://www.shwapno.com/SearchResults.aspx?search='+search_key
        self.driver.get(self.main_url)
        self.select_area(area)
        sleep(1)
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

        all_prods = soup.find_all('div', {'class': 'bucket'})

        p_list = []

        for x in all_prods:
            name = x.find('h4', {'class': 'mtb-title'}).string
            if not re.search(self.search_str, name, re.IGNORECASE):
                continue
            link = x.find('div', {'class': 'bucket_left'}).find('a')['href']
            img = x.find('div', {'class': 'bucket_left'}).find('img', attrs={"original":True})['original']
            price = x.find('label', {'class': 'mtb-ofr'}).find('span', {'class', 'sp_amt'}).string
            p = Product(name, price, 'Shwapno', link, img)
            p_list.append(p)


        return p_list






if __name__ == '__main__':
    app = Shwapno('butter', 'Uttara')

