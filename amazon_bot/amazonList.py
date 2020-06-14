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
import re
import calendar;
import time;




CHROMEDRIVER_PATH = './chromedriver/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

elements_to_return = 10
# driver = webdriver.Chrome(
#     # executable_path=CHROMEDRIVER_PATH,
#     options=chrome_options
# )


class AmazonList:
    __affiliate_id = "techdiscoun09-21"
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
        found = li.span
        return found.string.replace('#','') if found else ""

    def __gettitle(self, li):
        found = li.find('div', class_="p13n-sc-truncated")
        return found.string if found else ""

    def __getreviews(self, li):
         # could be not available for some items
        found = li.find('a', class_="a-size-small a-link-normal")
        return found.string if found else ""
        
    def __getlink(self, li):
        found = li.find('a', class_="a-link-normal")
        return found.get('href') if found else ""

    def __getprice(self, li): 
        found = li.find('span', class_="p13n-sc-price")
        return found.string if found else ""
    
    def __getimglink(self, li): 
        found = li.find('img')
        return found['src'] if found else ""
    
    def __getasin(self, link): 
        try:
            asin_found = re.search('/dp/(.+?)/ref', link).group(1)
        except AttributeError:
            asin_found = ''
        return asin_found

    def __getaffiliatelink(self, asin): 
        base_link = "https://www.amazon.it/dp/ASIN_TO_INCLUDE/ref=nosim?tag=" + self.__affiliate_id
        return base_link.replace("ASIN_TO_INCLUDE", asin)
    
    def __getTimesmp(self):
        ts = calendar.timegm(time.gmtime())
        return ts

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
        print("im ready")
        lilist = soup.find_all('span', class_='a-list-item')
        for li in lilist:
            position = self.__getposition(li)
            title    = self.__gettitle(li)
            reviews  = self.__getreviews(li)
            price    = self.__getprice(li)
            imglink  = self.__getimglink(li)
            link     = self.__getlink(li) ## not used in the object but useful to create other values (afflink, asin)
            asin     = self.__getasin(link)
            affLink  = self.__getaffiliatelink(asin)
            timesmp  = self.__getTimesmp()
            

            # object that will be pushed on mongodb
            itemToPush = {
                "position"      : position,
                "title"         : title, 
                "reviews"       : reviews,
                "price"         : price, 
                "imglink"       : imglink, 
                "link"          : link,
                "asin"          : asin,
                "affiliateLink" : affLink, 
                "timestamp"     : timesmp
            }

            itemObjList.append(itemToPush)
        
        #cut first n elements
        return itemObjList[:elements_to_return]

   

    def closeDriver(self):
        driver.quit()
        
