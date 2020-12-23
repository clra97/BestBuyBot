import os
import requests
from bs4 import BeautifulSoup
import time

class Scraper:

    def __init__(self, item):
#---Variables--------------------------------------
        self._timeout = 5               #used for connection functions (waits 10 seconds)
        self._wait = 1                  #used for speed at which we check each link (0 seconds)
#---Used-to-Scrape---------------------------------
        self._item = item                #item being searched
        self._url = None                #url
        self._headers = None            #headers for requests
        self._site = None               #response from request
        self._soup = None               #beautifulsoup object
#---Used-for-Dictionary----------------------------
        self._itemDictList = []          #List of GPU Dictionaries
        self._itemDict = {}              #Dictionary of GPU
#---Used-for-Messages------------------------------
        self._message = "Card Scraper Ready\n"  #message first displayed
        print(self._message)                    #prints message

#---Functions--------------------------------------
    def genSearchURL(self, page):
        self.url = "https://www.bestbuy.com/site/searchpage.jsp?cp={}&st={}".format(page, self.item)
    #used to create proper URLs for ease later on
    def genItemURL(self, url):
        return "https://www.bestbuy.com{}".format(url)

#---Connection-------------------------------------
    #one method to complete handshake and make soup to scrape
    def prepareSoup(self, headers):
        self.url = self.url                                         #creates URL to connect
        self.headers = headers                                      #use headers provided

        handshake = self.handshake()                                #request connection
        soup = self.makeSoup()                                      #create soup from connection to parse

        if handshake and soup:
            return True
        else:
            return False
    #request website in while loop 
    def handshake(self):
        response = False

        while response == False:                                    #while loop to try requesting website
            try:                                                    #used incase of errors
                self.site = requests.get(self.url,                  #url
                                    headers=self.headers,           #headers
                                        timeout=self.timeout)       #timeout (10 seconds)
                response = True
            except:
                print("{} - There was an error connecting!\nTry again!\n".format(self.site)) #prints status code
                time.sleep(self.timeout)

        if str(self.site) == "<Response [200]>":
            print("{} - Successful!\n".format(self.site))           #status code: 200 = good
            return True
        else:
            print("{} - No Items to scrape!\n".format(self.site))   #status code other than 200 = bad
            return False
    #create beautifulsoup with try and except
    def makeSoup(self):
        response = False #used to break loop to connect

        print("Creating Soup...\n") #message to let user know processing

        while response == False: #while loop to try creating soup
            try: #used in case of errors
                self.soup = BeautifulSoup(self.site.content, #creates BeautifulSoup Object from request
                                        'lxml')             #parses with lxml library (Fastest)

                print("Successful!\n")

                response = True #will break loop
            except:
                print("There was an error making soup!\nTry again!\n")
                time.sleep(self.timeout)

        return True

#---create-gpuDict---------------------------------
    #create GPU Dictionary by scraping text off link
    def createItemDict(self):
        for item in self.soup.find_all('li', "sku-item"):                   #find List of GPUs on search
            for link in item.find(class_='sku-header'):                     #once found go through each GPU

                name = link.text                                            #capture Name of GPU
                url = link.get('href')                                      #capture URL of GPU

                if url == None:
                    pass
                else:
                    self.itemDict = {'name' : name,                         #append name
                                    'url' : self.genItemURL(url),           #append URL
                                    'price' : None,                         #append Price (Default Value) 
                                    'in-stock' : None }                     #append Avail (Default Value)

                    self.itemDictList.append(self.itemDict)                 #append Dictionary to List of GPUs
                    
    def finishItemList(self):
        for items in self.itemDictList:
            name = items['name']
            url = items['url']

            self.prepareSoup(self.headers)

            items['price'] = self.checkPrice()
            items['in-stock'] = self.checkInstock()

        return self._itemDictList
    #checks page for specific text on price of GPU and then returns it
    def checkPrice(self):
        price = self.soup.find('div', 'priceView-hero-price priceView-customer-price').find('span').text
        return price
    #checks if specific card 
    def checkInstock(self):
        button = self.soup.find('div', 'fulfillment-add-to-cart-button').find('button').text
        
        if button == 'Sold Out' or button == 'Coming Soon':
            return False
        else:
            return True

    def sleep(self):
        self.clearDicts()
        time.sleep(60)

    def clearScreen(self):
        os.system("cls")

    def clearDicts(self):
        self.itemDictList.clear()
        self.itemDict.clear()

#---Getters----------------------------------------
    @property
    def timeout(self):
        return self._timeout
    @property
    def wait(self):
        return self._wait
    @property
    def item(self):
        return self._item
    @property
    def headers(self):
        return self._headers
    @property
    def url(self):
        return self._url
    @property
    def site(self):
        return self._site
    @property
    def soup(self):
        return self._soup
#---Dictionary-Getters-----------------------------
    @property
    def itemDictList(self):
        return self._itemDictList
    @property
    def itemDict(self):
        return self._itemDict
    @property
    def itemInstockList(self):
        return self._itemInstockList
#---Message-Getter---------------------------------
    @property
    def message(self):
        return self._message
#---Setters----------------------------------------
    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout
    @wait.setter
    def wait(self, wait):
        self._wait = wait
    @item.setter
    def item(self, item):
        self._item = item
    @headers.setter
    def headers(self, headers):
        self._headers = headers
    @url.setter
    def url(self, url):
        self._url = url
    @site.setter
    def site(self, site):
        self._site = site
    @soup.setter
    def soup(self, soup):
        self._soup = soup
#---Dictionary-Setters-----------------------------
    @itemDictList.setter
    def itemDictList(self, itemDictList):
        self._itemDictList = itemDictList
    @itemDict.setter
    def itemDict(self, itemDict):
        self._itemDict = itemDict
    @itemInstockList.setter
    def itemInstockSet(self, itemInstockList):
        self._itemInstockList = itemInstockList
#---Message-Setters--------------------------------
    @message.setter
    def message(self, message):
        self._message = message
#---Deleters---------------------------------------
    @timeout.deleter
    def timeout(self):
        self._timeout = None
    @wait.deleter
    def wait(self):
        self._wait = None
    @item.deleter
    def item(self):
        self._item = None
    @headers.deleter
    def headers(self):
        self._headers = None
    @url.deleter
    def url(self):
        self._url = None
    @site.deleter
    def site(self):
        self._site = None
    @soup.deleter
    def soup(self):
        self._soup = None
#---Dictionary-Deleters----------------------------
    @itemDictList.deleter
    def itemDictList(self):
        self._itemDictList = itemDictList
    @itemDict.deleter
    def itemDict(self):
        self._itemDict = {}
    @itemInstockList.deleter
    def itemInstockList(self):
        self._itemInstockList = []
#---Message-Deleters-------------------------------
    @message.deleter
    def message(self):
        self._message = "No Message"
