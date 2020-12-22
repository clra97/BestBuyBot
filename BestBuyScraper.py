from Scraper import *
import threading

#Returns the available items from best buy
def scrape(headers):

    scraper = BestBuyScraper()
    url = "/site/searchpage.jsp?st=3080"

    start_time = time.time()

    #Retreives html from URL
    scraper.prepareSoup(url, headers)

    #Clears the startup status messages
    scraper.clearScreen()

    #Create a dictionary of GPUs from the site
    scraper.createListings()

    # Create worker threads and start them
    scraper.makeWorkers()

    #Waits until all threads have completed their task
    main_thread = threading.current_thread()

    for t in threading.enumerate():
        if t is main_thread:
            continue
        print("joining ", t.getName())
        t.join()

    print("Program took: ", (time.time() - start_time))

    #Print the in stock GPUs
    return scraper.gpuDictList

class BestBuyScraper(Scraper):

    def __init__(self):
        super().__init__()

    # create GPU Dictionary by scraping text off link
    def createGPUList(self):
        for item in super().soup.find_all('li', "sku-item"):               #find List of GPUs on search
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

                super().listQueue.put(gpuDict)                        #Add dictionary to queue

#Getters-----------------------------------------------
    @property
    def gpuDictList(self):
        return super().gpuDictList
