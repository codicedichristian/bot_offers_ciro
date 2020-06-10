from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from itertools import *
from item import Item
import json



CHROMEDRIVER_PATH = './chromedriver/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# driver = webdriver.Chrome(
#     # executable_path=CHROMEDRIVER_PATH,
#     options=chrome_options
# )


class AmazonList:

    __items_to_get = 5
    # URL USED -> MAYBE COULD BE TRANSFERRED IN AN EXCEL FILE -> TO DO? 
    __categories = {

        ## BEST SELLER 24H HOURLY REFRESHED -- IMPORTANT
        "BEST_SELLER_GROCER_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/grocery/ref=zg_bsms_nav_0',
        "BEST_SELLER_KITCHE_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/kitchen/ref=zg_bsms_nav_gro_1_gro', 
        "BEST_SELLER_ELECTR_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/electronics/ref=zg_bsms_nav_1_amazon-devices',
        "BEST_SELLER_TOOLSS_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/tools/ref=zg_bsms_nav_ce_1_ce',
        "BEST_SELLER_COMPUT_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/pc/ref=zg_bsms_nav_light_1_light',
        "BEST_SELLER_SPORTS_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/sports/ref=zg_bsms_nav_s_1_s',
        
        ## BEST SELLER NEW LAUNCHED ITEMS HOURLY REFRESHED -- MEDIUM IMPORTANT 
        "BEST_LAUNCH_GLOBAL_HOURLY" : 'https://www.amazon.it/gp/bestsellers/boost/ref=zg_bs_nav_0',
        "BEST_LAUNCH_ELECTR_HOURLY" : 'https://www.amazon.it/gp/bestsellers/boost/14606289031/ref=zg_bs_nav_1_boost',
        "BEST_LAUNCH_KITCHE_HOURLY" : 'https://www.amazon.it/gp/bestsellers/boost/14606298031/ref=zg_bs_nav_3_14606302031',
        "BEST_LAUNCH_FOODNB_HOURLY" : 'https://www.amazon.it/gp/bestsellers/boost/14606304031/ref=zg_bs_nav_1_boost',
        
        ## BEST SELLER OF ALWAYS HOURLY REFRESHED -- LESS IMPORTANT
        "BEST_SELLER_GROCER_HOURLY" : "https://www.amazon.it/gp/bestsellers/grocery/ref=zg_bs_nav_0",
        "BEST_SELLER_KITCHE_HOURLY" : "https://www.amazon.it/gp/bestsellers/kitchen/ref=zg_bs_nav_0",
        "BEST_SELLER_LIGHTI_HOURLY" : "https://www.amazon.it/gp/bestsellers/lighting/ref=zg_bs_nav_0",
        "BEST_SELLER_ELECTR_HOURLY" : "https://www.amazon.it/gp/bestsellers/electronics/ref=zg_bs_nav_0",
        "BEST_SELLER_HCPHCP_HOURLY" : "https://www.amazon.it/gp/bestsellers/hpc/ref=zg_bs_nav_0"
    }

    # grouped array with this function 
    def __chunk(self, it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    # grouped items
    def __getItems(self, n, itemsArray):
        return list(self.__chunk(itemsArray, 4))[:n]

    def __getposition(self, li):
        return li.span.string.replace('#','')

    def __gettitle(self, li):
        return li.find('div', class_="p13n-sc-truncated").string

    def __getreviews(self, li):
         # could be not available for some items
        reviews = li.find('a', class_="a-size-small a-link-normal")
        if(reviews): 
            return reviews.string
        else: 
            return "0"
        
    def __getlink(self, li):
        return li.find('a', class_="a-link-normal").get('href')

    def getNewList(self, category_to_get): 

        ## get the correct link and call the browser and do the request
        link_to_use = self.__categories[category_to_get]
        pageResult = driver.get(link_to_use)
        timeout = 120
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "zg-ordered-list")))
        except TimeoutException:
            driver.quit()

        # get the listed items from html
        itemObjList = []
        # some = driver.find_elements_by_xpath('//*[@class="zg-item-immersion"]')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        lilist = soup.find_all('span', class_='a-list-item')
        for li in lilist:
            position = self.__getposition(li)
            title    = self.__gettitle(li)
            reviews  = self.__getreviews(li)
            link     = self.__getlink(li)
              #     # best_seller_obj = {
        #     #     "position" : float(group[0].replace('#',''))  , 
        #     #     "title" : group[1], 
        #     #     "review" : float(group[2]), 
        #     #     "price" : group[3]
        #     # }

        #     # #stringfy_obj = json.dumps(best_seller_obj, ensure_ascii=False).encode('utf8') ## json string
        #     # itemObjList.append(best_seller_obj)
        
        driver.quit()
        return 0
       
        # itemsArray = listedObjs.split('\n')
        # items_to_get = self.__items_to_get
        # subGroupedItems = self.__getItems(items_to_get, itemsArray)
        # driver.quit()
      
        
        # for group in subGroupedItems:
        #     print(group)
        #     # ## format things and put it into the final array 
        #     # best_seller_obj = {
        #     #     "position" : float(group[0].replace('#',''))  , 
        #     #     "title" : group[1], 
        #     #     "review" : float(group[2]), 
        #     #     "price" : group[3]
        #     # }

        #     # #stringfy_obj = json.dumps(best_seller_obj, ensure_ascii=False).encode('utf8') ## json string
        #     # itemObjList.append(best_seller_obj)
        

    def aggiornaListaContainers(self, container_name):
        #TODO: non so se serve
        return 0