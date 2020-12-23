import os
import requests
from bs4 import BeautifulSoup
import time
import queue
import validator as val

avail = False

class Scraper:

    def __init__(self):
#---Variables--------------------------------------
        self.timeout = 5                #used for connection functions (waits 10 seconds)
        self.wait = 0                   #used for speed at which we check each link (0 seconds)
#---Used-to-Scrape---------------------------------
        self.url = None                 #url
        self.headers = None             #headers for requests
        self.site = None                #response from request
        self.soup = None                #beautifulsoup object
#---Used-for-Dictionary----------------------------
        self.gpuInstockList = []        #In-stock GPUs
#---Used for threading-----------------------------
        self.threadLimit = 8            #Maximum Number of threads
        self.listQueue = None           #Queue used to give jobs to threads
#---Used-for-Messages------------------------------
        self.message = "Card Scraper Ready\n"  #message first displayed
        print(self.message)                    #prints message

#---Functions--------------------------------------
    #used to create proper URLs for ease later on
    def genURL(self, url):
        return "https://www.bestbuy.com{}".format(url)

#---Connection-------------------------------------

    #one method to complete handshake and make soup to scrape
    def prepareSoup(self, url, headers):
        self.url = self.genURL(url)     #creates URL to connect
        self.headers = headers          #Sets the headers to connect
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
            worker = val.GPUValidator(self.listQueue, self.gpuInstockList, self.headers, i)
            worker.start()

    # create GPU Dictionary by scraping text off link
    def createListings(self):
        for item in self.soup.find_all('li', "sku-item"):               #find List of GPUs on search
            for link in item.find(class_='sku-header'):                 #once found go through each GPU

                name = link.text                            #capture Name of GPU
                url = link.get('href')                      #capture URL of GPU

                #If url doesn't exist, skip
                if url == None:
                    continue

                gpuDict = { 'name' : name,                 #append name
                            'url' : url,                   #append URL
                            'price' : None,                #append Price (Default Value)
                            'in-stock' : False }           #append Avail (Default Value)

                self.listQueue.put(gpuDict)                        #Add dictionary to queue


    def printInstock(self):
        self.clearScreen()
        if len(self.gpuInstockList) > 0:
            print("Available:\n")
            for items in self.gpuInstockList:
                print("{}\n".format(items['name'])
                     +"Link: {}\n".format(self.genURL(items['url'])))

    def sleep(self):
        print("Will Continue in 1 minute...\n")
        time.sleep(60)

    def clearScreen(self):
        os.system("cls")
