from selenium import webdriver
#from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from itertools import *
from item import Item
import re
import calendar;
import time;


class AmazonList:

    __chrome_options = Options()
    __chrome_options.add_argument("--headless")
    __chrome_options.add_argument("--single-process")
    __chrome_options.add_argument("--no-sandbox")
    __chrome_options.add_argument("--disable-dev-shm-usage")
    __chrome_prefs = {}
    __chrome_options.experimental_options["prefs"] = __chrome_prefs
    __chrome_prefs["profile.default_content_settings"] = {"images": 2}
    __driver = webdriver.Chrome(options=__chrome_options)
    # #driver = webdriver.Chrome('/usr/bin/chromedriver')
    __elements_to_return =  25

    __affiliate_id = "dealsitalia0f-21"
    __categories = {
     #todo "BEST_SELLER_GROCER_HOURLY_24H" : "https://www.amazon.it/blackfriday/ref=gbps_fcr___wht_52399703?nocache=1605438649865&gb_f_GB-SUPPLE=dealTypes:DEAL_OF_THE_DAY%252CLIGHTNING_DEAL%252CBEST_DEAL,sortOrder:BY_DISCOUNT_DESCENDING,priceRanges:20-50,dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,minRating:3,discountRanges:10-25%252C25-50%252C50-70%252C70-,enforcedCategories:1497228031%252C524015031%252C2844433031%252C435504031%252C425916031%252C473365031%252C412609031%252C2454160031%252C6377736031%252C6198092031%252C732998031%252C473287031%252C635016031%252C435505031%252C524009031%252C524012031%252C524006031%252C412603031%252C12472499031%252C1571292031%252C14437356031&ie=UTF8",    
        "BEST_SELLER_GROCER_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/grocery/ref=zg_bsms_nav_0',
        "BEST_SELLER_KITCHE_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/kitchen/ref=zg_bsms_nav_gro_1_gro', 
        "BEST_SELLER_ELECTR_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/electronics/ref=zg_bsms_nav_1_amazon-devices',
        "BEST_SELLER_TOOLSS_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/tools/ref=zg_bsms_nav_ce_1_ce',
        "BEST_SELLER_COMPUT_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/pc/ref=zg_bsms_nav_light_1_light',
        "BEST_SELLER_SPORTS_HOURLY_24H" : 'https://www.amazon.it/gp/movers-and-shakers/sports/ref=zg_bsms_nav_s_1_s',
        
        #new 
        "BEST_SELLER_BOOSTT_HOURLY_24H"       : "https://www.amazon.it/gp/movers-and-shakers/boost/ref=zg_bsms_nav_gro_1_gro",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG1" : "https://www.amazon.it/gp/goldbox/ref=gbps_ftr_s-5_8ffd_acr_4?gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,sortOrder:BY_DISCOUNT_DESCENDING,enforcedCategories:1497228031%252C473287031%252C473365031%252C732997031%252C435505031%252C635016031%252C412609031%252C1571292031%252C425916031%252C524009031%252C524006031%252C2454148031%252C412603031%252C524012031,minRating:4,primeEligibleOnly:true&pf_rd_p=3dcc9ba5-cb56-42e1-ac1e-c26f3b278ffd&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A11IL2PNWYJU7H&pf_rd_r=CBZ0HSMMNKXCQPWT5TM7&ie=UTF8",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG2" : "https://www.amazon.it/gp/goldbox/ref=gbps_ftr_s-5_8ffd_page_2?gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,page:2,sortOrder:BY_DISCOUNT_DESCENDING,enforcedCategories:1497228031%252C473287031%252C473365031%252C732997031%252C435505031%252C635016031%252C412609031%252C1571292031%252C425916031%252C524009031%252C524006031%252C2454148031%252C412603031%252C524012031,minRating:4,primeEligibleOnly:true,dealsPerPage:40&pf_rd_p=3dcc9ba5-cb56-42e1-ac1e-c26f3b278ffd&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A11IL2PNWYJU7H&pf_rd_r=CBZ0HSMMNKXCQPWT5TM7&ie=UTF8",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG3" : "https://www.amazon.it/gp/goldbox/ref=gbps_ftr_s-5_8ffd_page_3?gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,page:3,sortOrder:BY_DISCOUNT_DESCENDING,enforcedCategories:1497228031%252C473287031%252C473365031%252C732997031%252C435505031%252C635016031%252C412609031%252C1571292031%252C425916031%252C524009031%252C524006031%252C2454148031%252C412603031%252C524012031,minRating:4,primeEligibleOnly:true,dealsPerPage:40&pf_rd_p=3dcc9ba5-cb56-42e1-ac1e-c26f3b278ffd&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A11IL2PNWYJU7H&pf_rd_r=CBZ0HSMMNKXCQPWT5TM7&ie=UTF8",
        "DEALS_BEST_SELLER_MIX____HOURLY_L20" : "https://www.amazon.it/gp/goldbox/ref=gbps_ftr_s-5_8ffd_prc_-20?gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL,sortOrder:BY_DISCOUNT_DESCENDING,enforcedCategories:1497228031%252C473287031%252C473365031%252C732997031%252C435505031%252C635016031%252C412609031%252C1571292031%252C425916031%252C524009031%252C524006031%252C2454148031%252C412603031%252C524012031,minRating:4,primeEligibleOnly:true,priceRanges:-20&pf_rd_p=3dcc9ba5-cb56-42e1-ac1e-c26f3b278ffd&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A11IL2PNWYJU7H&pf_rd_r=CBZ0HSMMNKXCQPWT5TM7&ie=UTF8",
 
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
        # remove last piece to get high quality
        return found['src'].replace("._AC_UL200_SR200,200_","") if found else ""
    
    def __getasin(self, link): 
        try:
            asin_found = re.search('(dp|deal)\/(.+?)\/ref', link).group(2)
        except AttributeError:
            asin_found = ''
        return asin_found

    def __getaffiliatelink(self, asin, link): 
        base_link = "https://www.amazon.it/" + link + "&tag=" + self.__affiliate_id
        return base_link

    def __getaffiliatelink(self, asin, link): 
       if "/dp/" in link: 
           base_link = "https://www.amazon.it/dp/ASIN_TO_INCLUDE/ref=nosim?tag=" + self.__affiliate_id
           return base_link.replace("ASIN_TO_INCLUDE", asin)
              
       return "https://www.amazon.it/" + link.replace("https://www.amazon.it/", "") + "&ref=nosim?tag=" + self.__affiliate_id
        
    def __getTimesmp(self):
        ts = calendar.timegm(time.gmtime())
        return ts
    
    def __getDealslink(self, li):
        found = li.find('a', class_="a-link-normal")
        return found.get('href') if found else ""

    def __getDealsPrezzoOfferta(self, li):
        found = li.find('span', class_="dealPriceText")
        return found.string if found else ""

    def __getDealsInveceDi(self, li): 
        completo = ""
        found = li.find("div", class_="a-spacing-top-mini")
        if found: 
            spans = found.find_all('span')
            for span in spans: 
                replacedSpan = span.text.replace(":","").replace("\n","").replace(" ","")
                completo = completo + replacedSpan + ":"
        return completo.replace("\n", "")

    def __getDealsTitle(self, li): 
        found = li.find('a', class_="singleCellTitle")
        if found:
            return found.find('span').string.replace('\n', '')
        else: return ""
    
    def __getDealsImgLink(self, li):
        found = li.find("img")
        #print(found['src']) if found else print("")
        #print(re.sub("(\._.*_.jpg)", ".jpg", found['src']))
        return re.sub("(\._.*_.jpg)", ".jpg", found['src']) if found else "" 

    def getNewList(self, category_to_get): 

        ## get the correct link and call the browser and do the request
        link_to_use = self.__categories[category_to_get]
        pageResult = self.__driver.get(link_to_use)
        timeout = 220
        ### non so dove sono andati a finire. 
        if "DEALS" in category_to_get: 
            try:
                print("get objs from deals link")
                WebDriverWait(self.__driver, timeout).until(EC.visibility_of_element_located((By.ID, "widgetContent")))
            except TimeoutException:
                print("timeout exception driver will be closed")
                self.__driver.quit()
            
            # get the listed items from html
            itemObjList = []
            soup = BeautifulSoup(self.__driver.page_source, 'html.parser')

            lilist = soup.find_all('div', "singleCell")

            if(len(lilist) == 0): 
                print("nothing") 
                return
            else:
                for li in lilist:
                    link = self.__getDealslink(li)
                    price = self.__getDealsPrezzoOfferta(li)
                    inveceDi= self.__getDealsInveceDi(li)
                    title= self.__getDealsTitle(li)
                    asin = self.__getasin(link)
                    affLink  = self.__getaffiliatelink(asin, link)
                    timesmp  = self.__getTimesmp()
                    imgLink = self.__getDealsImgLink(li)
                  
                    itemToPush = {
                            "position"      : "",
                            "title"         : title, 
                            "reviews"       : "",
                            "price"         : price, 
                            "imglink"       : imgLink, 
                            "link"          : link,
                            "asin"          : asin,
                            "affiliateLink" : affLink, 
                            "timestamp"     : timesmp,
                            "inveceDi"      : inveceDi, 
                        }

                    itemObjList.append(itemToPush)
            
                    #cut first n elements
                    
                return itemObjList[:30]

        else:
            try:
                WebDriverWait(self.__driver, timeout).until(EC.visibility_of_element_located((By.ID, "zg-ordered-list")))
            except TimeoutException:
                print("timeout exception driver will be closed")
                self.__driver.quit()

            # get the listed items from html
            itemObjList = []
            # some = driver.find_elements_by_xpath('//*[@class="zg-item-immersion"]')
            soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
            
            lilist = soup.find_all('span', class_='a-list-item')
            for li in lilist:
                position = self.__getposition(li)
                title    = self.__gettitle(li)
                reviews  = self.__getreviews(li)
                price    = self.__getprice(li)
                imglink  = self.__getimglink(li)
                link     = self.__getlink(li) ## not used in the object but useful to create other values (afflink, asin)
                asin     = self.__getasin(link)
                affLink  = self.__getaffiliatelink(asin, link)
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
                    "timestamp"     : timesmp,
                    "inveceDi"      : "",
                }

                itemObjList.append(itemToPush)
            
            #cut first n elements
            return itemObjList[:self.__elements_to_return]

   

    def closeDriver(self):
        self.__driver.quit()
        
