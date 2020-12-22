from Listing import *

# Class for holding the html of and examinging a GPU listing
class GPUListing(Listing):

    def __init__(self):
        super().__init__()

    #checks page for specific text on price of GPU and then returns it
    def checkPrice(self):
        return super().soup.find('div', 'priceView-hero-price priceView-customer-price').find('span').text

    #checks if specific card
    def checkInstock(self):
        button = super().soup.find('div', 'fulfillment-add-to-cart-button').find('button').text

        if button == 'Sold Out' or button == 'Coming Soon':
            return False
        else:
            return True

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
                return 1

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
