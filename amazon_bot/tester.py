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

link_to_use = "https://www.amazon.it/deal/06ea9066/ref=gbps_tit___06ea9066?showVariations=true&BFDay=true&smid=A11IL2PNWYJU7H"
pageResult = driver.get(link_to_use)
timeout = 5


def getlink(li):
    found = li.find('a', class_="a-link-normal")
    return found.get('href') if found else ""

def getPrezzoOfferta(li):
    found = li.find('div', class_="a-row octopus-dlp-price")
    completo=""
    if found: 
        spans = found.find_all('span')
        some = spans[3]
        return some.text if some else ""
    return ""
        

def getInveceDi(li): 
        completo = ""
        found = li.find("span", class_="octopus-widget-price-saving-info")
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
    found = li.find('span', class_="a-size-base a-color-base").find('span')
    return found.string if found else ""

def getasin(link): 
    try:
        asin_found = re.search('(dp|deal)\/(.+?)\/ref', link).group(2)
    except AttributeError:
        asin_found = ''
    return asin_found

try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "octops-dlp-asin-stream-section")))
except TimeoutException:
    print("timeout exception driver will be closed")
    driver.quit()

soup = BeautifulSoup(driver.page_source, 'html.parser')
lilist = soup.find_all('li', "a-list-normal")
if(len(lilist) == 0): 
   print("nothing") 
else:
    for li in lilist:
        print(li)
        link = getlink(li)
        prezzoOfferta = getPrezzoOfferta(li)
        inveceDi= getInveceDi(li)
        title= getTitle(li)
        asin = getasin(link)
        affLink = getaffiliatelink(asin, link)
        print(affLink, prezzoOfferta, inveceDi, title)
        print("\n___________________________\n")