import BestBuyScraper as best

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

scrapers = [best]

availableItems = []

#Run all scrapers
for scraper in scrapers:
    availableItems.append(scraper.scrape(headers))

#Sort available available items

#Display available items
print("Available items: ", availableItems)
