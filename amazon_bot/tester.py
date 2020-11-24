from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from itertools import *
import re

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome(executable_path='/Users/christian/personalProjects/best_deals_amz/amazon_bot/chromedriver')
elements_to_return = 10

link_to_use = "https://www.amazon.it/blackfriday/2/ref=gbps_ftr___sort_BSEL?gb_f_GB-SUPPLE=enforcedCategories:473287031%252C435504031%252C732998031%252C6198092031%252C6377736031%252C524015031%252C1497228031%252C473365031%252C827181031%252C435505031%252C635016031%252C14437356031%252C425916031%252C524009031%252C524006031%252C524012031%252C2844433031%252C412609031%252C1571292031%252C10272111,dealTypes:DEAL_OF_THE_DAY%252CLIGHTNING_DEAL%252CBEST_DEAL,discountRanges:10-25%252C25-50%252C50-70%252C70-,minRating:3,sortOrder:BY_BEST_SELLING,dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL&gb_ttl_GB-SUPPLE=Offerte%2520a%2520Meno%2520di%252020%E2%82%AC&ie=UTF8"
pageResult = driver.get(link_to_use)
timeout = 5

try:
    print("trying")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "widgetContent")))
except TimeoutException:
    print("timeout exception driver will be closed")
    driver.quit()

def getlink(li):
    found = li.find('a', class_="a-link-normal")
    return found.get('href') if found else ""

def getPrezzoOfferta(li):
    found = li.find('span', class_="dealPriceText")
    return found.string if found else ""

def getInveceDi(li): 
        completo = ""
        found = li.find("div", class_="a-spacing-top-mini")
        if found: 
            spans = found.find_all('span')
            for span in spans: 
                replacedSpan = span.text.replace(":","").replace("\n","").replace(" ","")
                completo = completo + replacedSpan + ":"
        return completo.replace("\n", "")

def getaffiliatelink(asin, link): 
    affiliate_id = "dealsitalia0f-21"
    if "/dp/" in link: 
        base_link = "https://www.amazon.it/dp/ASIN_TO_INCLUDE/ref=nosim?tag=" + affiliate_id
        return base_link.replace("ASIN_TO_INCLUDE", asin)
    if "/deal" in link: 
        base_link = "https://www.amazon.it/deal/ASIN_TO_INCLUDE/ref=nosim?tag=" + affiliate_id
        return base_link.replace("ASIN_TO_INCLUDE", asin)
    return ""
        

def getTitle(li): 
    found = li.find('a', class_="singleCellTitle").find('span')
    return found.string if found else ""

def getasin(link): 
    try:
        asin_found = re.search('(dp|deal)\/(.+?)\/ref', link).group(2)
    except AttributeError:
        asin_found = ''
    return asin_found

try:
    print("get objs from deals link")
    
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "widgetContent")))
except TimeoutException:
    print("timeout exception driver will be closed")
    driver.quit()
soup = BeautifulSoup(driver.page_source, 'html.parser')
lilist = soup.find_all('div', "singleCell")
if(len(lilist) == 0): 
   print("nothing") 
else:
    for li in lilist:
        link = getlink(li)
        prezzoOfferta = getPrezzoOfferta(li)
        inveceDi= getInveceDi(li)
        title= getTitle(li)
        asin = getasin(link)
        affLink = getaffiliatelink(asin, link)
        print(affLink, prezzoOfferta, inveceDi, title)
        print("\n___________________________\n")