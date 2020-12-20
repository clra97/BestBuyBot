import os
import requests
from bs4 import BeautifulSoup
import time
import queue
import validator as val

class CardScrapper:

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
        self._gpuDictList = []          #List of GPU Dictionaries
        self._gpuInstockList = []       #In-stock GPUs
#---Used for threading-----------------------------
        self._threadLimit = 8           #Maximum Number of threads
        self._listQueue = None          #Queue used to give jobs to threads
        self._threadList = []           #List of threads
#---Used-for-Messages------------------------------
        self._message = "Card Scraper Ready\n"  #message first displayed
        print(self._message)                    #prints message

#---Functions--------------------------------------
    #used to create proper URLs for ease later on
    def genURL(self, url):
        return "https://www.bestbuy.com{}".format(url)

#---Connection-------------------------------------

    #one method to complete handshake and make soup to scrape
    def prepareSoup(self, url, headers):
        #self.printInstock()
        self.url = self.genURL(url)     #creates URL to connect
        self.headers = headers          #use headers provided
        self.listQueue = queue.Queue()  #Instantiates the job queue for threads

        self.handshake()                #request connection
        self.makeSoup()                 #create soup from connection to parse

    #request website in while loop
    def handshake(self):
        response = False

        while response == False: #while loop to try requesting website
            try: #used incase of errors
                self.site = requests.get(self.url,            #url
                                         headers=self.headers,#headers
                                         timeout=self.timeout)#timeout (10 seconds)
                print("{} - Successful!\n".format(self.site)) #prints status code: 200 = good
                response = True #breaks loop
            except:
                print("{} - There was an error connecting!\nTry again!\n".format(self.site)) #prints status code
                time.sleep(self.timeout)

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

    # Create worker threads and start them
    def makeWorkers(self):
        for i in range(self.threadLimit):
            worker = val.GPUValidator(self.listQueue, i)
            self.threadList.append(worker)
            worker.start()

    # create GPU Dictionary by scraping text off link
    def createGPUList(self):
        for item in self.soup.find_all('li', "sku-item"):               #find List of GPUs on search
            for link in item.find(class_='sku-header'):                 #once found go through each GPU

                name = link.text                            #capture Name of GPU
                url = link.get('href')                      #capture URL of GPU

                gpuDict = { 'name' : name,                 #append name
                            'url' : url,                   #append URL
                            'price' : None,                #append Price (Default Value)
                            'in-stock' : False }           #append Avail (Default Value)

                self.appendGPUDict(gpuDict)                        #append Dictionary to List of GPUs
                self.listQueue.put(gpuDict)                        #Add dictionary to queue

    #append dictionary created from function to list
    def appendGPUDict(self, gpuDict):
        self.gpuDictList.append(gpuDict) #appends to list

    def checkGPUList(self):

        for items in self.gpuDictList:
            name = items['name']
            url = items['url']

            self.prepareSoup(url, self.headers)

            items['price'] = self.checkPrice()
            items['in-stock'] = self.checkInstock()

            if items['in-stock'] == True:
                self.addInstock(items)
                if name == "NVIDIA GeForce RTX 3080 10GB GDDR6X PCI Express 4.0 Graphics Card - Titanium and Black":
                    return True
                else:
                    time.sleep(self.wait)
                    pass
            else:
                print("Not In-Stock...\n")
                time.sleep(self.wait)
                pass

            self.printInstock()

        return False

    def sleep(self):
        print("Will Continue in 1 minute...\n")
        time.sleep(60)

    def printFinalDict(self):
        for items in self.gpuDict.items():
            print(items)

    def clearScreen(self):
        os.system("cls")

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
    def gpuDictList(self):
        return self._gpuDictList
    @property
    def gpuDict(self):
        return self._gpuDict
    @property
    def gpuInstockList(self):
        return self._gpuInstockList
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
#---Thread-Getters---------------------------------
    @property
    def threadLimit(self):
        return self._threadLimit
    @property
    def listQueue(self):
        return self._listQueue
    @property
    def threadList(self):
        return self._threadList
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
    @gpuDictList.setter
    def gpuDictList(self, gpuDictList):
        self._gpuDictList = gpuDictList
    @gpuDict.setter
    def gpuDict(self, gpuDict):
        self._gpuDict = gpuDict
    @gpuInstockList.setter
    def gpuInstockSet(self, gpuInstockList):
        self._gpuInstockList = gpuInstockList
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
#---Thread-Setters---------------------------------
    @threadLimit.setter
    def threadLimit(self, threadLimit):
        self._threadLimit = threadLimit
    @listQueue.setter
    def listQueue(self, listQueue):
        self._listQueue = listQueue
    @threadList.setter
    def threadList(self, threadList):
        self._threadList = threadList
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
    @gpuDictList.deleter
    def gpuDictList(self):
        self._gpuDictList = gpuDictList
    @gpuDict.deleter
    def gpuDict(self):
        self._gpuDict = {}
    @gpuInstockList.deleter
    def gpuInstockList(self):
        self._gpuInstockList = []
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
#---Thread-Deleters--------------------------------
    @threadLimit.deleter
    def threadLimit(self):
        self._threadLimit = None
    @listQueue.deleter
    def listQueue(self):
        self._listQueue = None
    @threadList.deleter
    def threadList(self):
        self._threadList = None
#---Message-Deleters-------------------------------
    @message.deleter
    def message(self):
        self._message = "No Message"
