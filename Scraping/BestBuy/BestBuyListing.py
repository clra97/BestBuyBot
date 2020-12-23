import Listing

# Class for holding the html of and examinging a GPU listing
class GPUListing(Listing):

    def __init__(self):
        super().__init__()

    #checks page for specific text on price of GPU and then returns it
    def checkPrice(self):
        return self.soup.find('div', 'priceView-hero-price priceView-customer-price').find('span').text

    #checks if specific card
    def checkInstock(self):
        button = self.soup.find('div', 'fulfillment-add-to-cart-button').find('button').text

        if button == 'Sold Out' or button == 'Coming Soon':
            return False
        else:
            return True
