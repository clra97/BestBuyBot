import threading
import os
import requests
import time
import queue
from bs4 import BeautifulSoup

# Class for holding the html of and examinging a GPU listing
class Listing():

    def __init__(self):
#---Variables--------------------------------------
        self.timeout = 5               #used for connection functions (waits 10 seconds)
#---Used-to-Scrape---------------------------------
        self.url = None                #url
        self.headers = None            #headers for requests
        self.site = None               #response from request
        self.soup = None               #beautifulsoup object
#---Used-for-Dictionary----------------------------
        self.gpuDict = {}              #Dictionary of GPU
#---Used for threading-----------------------------
        self.listQueue = None              #Queue used to give jobs to threads
#---Used-for-Messages------------------------------
        self.message = "Card Scraper Ready\n"  #message first displayed
        print(self.message)                    #prints message

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

        avail = False

    #checks page for specific text on price of GPU and then returns it
    def checkPrice(self):
        self.gpuDictPrice = self.soup.find('div', 'priceView-hero-price priceView-customer-price').find('span').text
        return self.gpuDictPrice

    #checks if specific card
    def checkInstock(self):
        button = self.soup.find('div', 'fulfillment-add-to-cart-button').find('button').text

        if button == 'Sold Out' or button == 'Coming Soon':
            return False
        else:
            return True

    def addInstock(self, items, inStockList):
        lock = threading.Lock()
        lock.acquire()

        if items not in inStockList:
            inStockList.append(items)

        lock.release()
