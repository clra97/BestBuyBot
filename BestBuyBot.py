import time
from CardScrapper import *

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
url = "/site/searchpage.jsp?st=3080"
avail = False

scraper = CardScrapper()

while avail == False:
    scraper.prepareSoup(url, headers)

    scraper.clearScreen()

    scraper.createGPUDict()

    avail = scraper.checkGPUList()

    scraper.sleep()
