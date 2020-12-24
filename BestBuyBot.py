import time
from Scraper import *

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
item = "3080"
threadLimit = 8
page = 1
run = True
scrape = True

programStart = time.perf_counter()
scraper = Scraper(item)

while scrape == True:
    pageStart = time.perf_counter()                         #time

    scraper.genSearchURL(page)                              #used for pages

    scrape = scraper.prepareSoup(headers)                   #connects to page

    scraper.searchDict()                                    #collects items from first search

    itemList = scraper.itemDict()                           #finalizes item properties

    #eventually write properties of each item to a file
    #track time of writing
    #check for duplicates
    #check page for lists when going to the next page

    # for item in itemList:
    #     print("Item: {}\n".format(item['name'])
    #          +"Price: {}\n".format(item['price'])
    #          +"URL: {}\n".format(item['url']))

    scraper.clearDicts()

    pageFinish = time.perf_counter()

    print("Results for page #{}:\n\n".format(page)
        +"{}\n\n".format(itemList)
        +"Time: {}\n".format(round(pageFinish-pageStart, 2)))

    page += 1

programFinish = time.perf_counter()
print("Done Scraping - {}seconds".format(round(programFinish-programStart, 2)))