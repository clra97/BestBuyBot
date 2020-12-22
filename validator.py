import threading
import os
import requests
import time
import queue
from bs4 import BeautifulSoup

# Class for holding the html of and examinging a GPU listing
class GPUListing():

    def __init__(self):
#---Variables--------------------------------------
        self._timeout = 5               #used for connection functions (waits 10 seconds)
        self._wait = 0                  #used for speed at which we check each link (0 seconds)
#---Used-to-Scrape---------------------------------
        self._url = None #url
        self._headers = None            #headers for requests
        self._site = None               #response from request
        self._soup = None               #beautifulsoup object
#---Used-for-Dictionary----------------------------
        self._gpuDict = {}              #Dictionary of GPU
#---Used for threading-----------------------------
        self._listQueue = None              #Queue used to give jobs to threads
#---Used-for-Messages------------------------------
        self._message = "Card Scraper Ready\n"  #message first displayed
        print(self._message)                    #prints message

#---Functions--------------------------------------
    #used to create proper URLs for ease later on
    def genURL(self, url):
        return "https://www.bestbuy.com{}".format(url)
#---Connection-------------------------------------

    #one method to complete handshake and make soup to scrape
    def prepareSoup(self, listing, headers):
        self.gpuDict = listing

        #self.printInstock()
        self.url = self.genURL(self.gpuDict['url'])  #sets the url to scrape
        self.headers = headers          #use headers provided

        self.handshake()                #request connection
        self.makeSoup()                 #create soup from connection to parse

    #request website in while loop
    def handshake(self):
        response = False

        print(threading.current_thread().number, " job: ", self.gpuDict)

        #while response == False: #while loop to try requesting website
        try: #used incase of errors
            self.site = requests.get(self.url,            #url
                                     headers=self.headers,#headers
                                     timeout=self.timeout)#timeout (10 seconds)
            print("{} - Successful!\n".format(self.site)) #prints status code: 200 = good
            response = True #breaks loop
        except:
            print(threading.current_thread().number, ": {} - There was an error connecting!\nTry again!\n".format(self.site)) #prints status code
            time.sleep(self.timeout)

    #create beautifulsoup with try and except
    def makeSoup(self):
        response = False #used to break loop to connect

        print("Creating Soup...\n") #message to let user know processing

        #while response == False: #while loop to try creating soup
        try: #used in case of errors
            self.soup = BeautifulSoup(self.site.content, #creates BeautifulSoup Object from request
                                     'lxml')             #parses with lxml library (Fastest)

            print("Successful!\n")

            response = True #will break loop
        except:
            print("There was an error making soup!\nTry again!\n")
            time.sleep(self.timeout)

    def checkAvail(self, inStockList):
        global avail
        #Get the dictionary of the current GPU listing
        gpu = self.gpuDict

        #Fill in the price and availability of the current listing
        gpu['price'] = self.checkPrice()
        gpu['in-stock'] = self.checkInstock()

        #Chech if the GPU is in stock
        if gpu['in-stock'] == True:
            self.addInstock(gpu, inStockList)
            if gpu['name'] == "NVIDIA GeForce RTX 3080 10GB GDDR6X PCI Express 4.0 Graphics Card - Titanium and Black":
                avail = True
        else:
            print(threading.current_thread().number, ": Not In-Stock...\n")
            time.sleep(self.wait)

        avail = False

    #checks page for specific text on price of GPU and then returns it
    def checkPrice(self):
        self.gpuDictPrice = self.soup.find('div', 'priceView-hero-price priceView-customer-price').find('span').text
        return self.gpuDictPrice

    #checks if specific card
    def checkInstock(self):
        button = self.soup.find('div', 'fulfillment-add-to-cart-button').find('button').text

        if button == 'Sold Out':# or 'Coming Soon':
            return False
        else:
            return True

    def addInstock(self, items, inStockList):
        lock = threading.Lock()
        lock.acquire()

        if items not in inStockList:
            inStockList.append(items)

        lock.release()

    def sleep(self):
        print("Will Continue in 1 minute...\n")
        time.sleep(60)

#---Getters----------------------------------------
    @property
    def timeout(self):
        return self._timeout
    @property
    def wait(self):
        return self._wait
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
    def gpuDict(self):
        return self._gpuDict
    @property
    def gpuDictName(self):
        return self._gpuDictName
    @property
    def gpuDictURL(self):
        return self._gpuDictURL
    @property
    def gpuDictPrice(self):
        return self._gpuDictPrice
    @property
    def gpuDictInstock(self):
        return self._gpuDictInstock
#---Queue-Getter-----------------------------------
    @property
    def listQueue(self):
        return self._listQueue
#---Message-Getter---------------------------------
    @property
    def message(self):
        return self._message

#---Setters----------------------------------------
    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout
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
    @gpuDict.setter
    def gpuDict(self, gpuDict):
        self._gpuDict = gpuDict
    @gpuDictName.setter
    def gpuDictName(self, gpuDictName):
        self._gpuDictName = gpuDictName
    @gpuDictURL.setter
    def gpuDictURL(self, gpuDictURL):
        self._gpuDictURL = gpuDictURL
    @gpuDictPrice.setter
    def gpuDictPrice(self, gpuDictPrice):
        self._gpuDictPrice = gpuDictPrice
    @gpuDictInstock.setter
    def gpuDictAvail(self, gpuDictInstock):
        self._gpuDictAvail = gpuDictInstock
#---Queue-Setter-----------------------------------
    @listQueue.setter
    def listQueue(self, listQueue):
        self._listQueue = listQueue
#---Message-Setters--------------------------------
    @message.setter
    def message(self, message):
        self._message = message

#---Deleters---------------------------------------
    @timeout.deleter
    def timeout(self):
        self._timeout = None
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
    @gpuDict.deleter
    def gpuDict(self):
        self._gpuDict = {}
    @gpuDictName.deleter
    def gpuDictName(self):
        self._gpuDictName = None
    @gpuDictURL.deleter
    def gpuDictURL(self):
        self._gpuDictURL = None
    @gpuDictPrice.deleter
    def gpuDictPrice(self):
        self._gpuDictPrice = None
    @gpuDictInstock.deleter
    def gpuDictInstock(self):
        self._gpuDictInstock = False
#---Queue-Deleter-----------------------------------
    @listQueue.deleter
    def listQueue(self):
        self._listQueue = None
#---Message-Deleters-------------------------------
    @message.deleter
    def message(self):
        self._message = "No Message"

#Reimplementation of threading class to check the listing of a GPU
class GPUValidator(threading.Thread):

    def __init__(self, gpuQueue, inStockList, headers, number):
        super().__init__()
        self.listing = GPUListing()
        self.inStockList = inStockList
        self.headers = headers
        self.gpuQueue = gpuQueue
        self.number = number

    def run(self):
        print("Starting thread: ", self.number)

        while not self.gpuQueue.empty():
            try:
                #Get the job from the given queue
                gpu = self.gpuQueue.get(timeout=self.listing.timeout)
            except queue.Empty:
                #If the queue is empty, the thread exits
                print("Queue is empty")
                return 0

            #Tells that the thread is done with the queue
            self.gpuQueue.task_done()

            print(self.number, " got job from Queue")

            #Attempt to make connection and retreive html
            #Should give up control to another thread
            self.listing.prepareSoup(gpu, self.headers)

            print("Thread: ", self.number, " prepared")

            #Set the price of the gpu if it's available
            self.listing.checkAvail(self.inStockList)

        return 1
