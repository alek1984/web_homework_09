import os

os.system("scrapy crawl quotes -O quotes.json")
os.system("scrapy crawl quotes -O authors.json")
