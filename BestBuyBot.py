import time
from Scraper import *

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
item = "3080"
page = 4
run = True
scrape = True

scraper = Scraper(item)

while scrape == True:
    scraper.genSearchURL(page)

    scrape = scraper.prepareSoup(headers)

    scraper.createItemDict() #threading needed

    itemList = scraper.finishItemList() #threading needed

    #eventually write properties of each item to a file
    #track time of writing
    #check for duplicates
    #check page for lists when going to the next page
    for item in itemList:
        print("Item: {}\n".format(item['name'])
             +"Price: {}\n".format(item['price'])
             +"URL: {}\n".format(item['url']))

    scraper.clearDicts()

    page += 1

print("Done Scraping")