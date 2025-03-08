import scrapy
from quotes_scraper.items import QuoteItem, AuthorItem
import json
import os

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]

    authors = {}

    def parse(self, response):
        # Парсимо цитати
        for quote in response.css("div.quote"):
            quote_item = QuoteItem()
            quote_item["quote"] = quote.css("span.text::text").get()
            quote_item["author"] = quote.css("small.author::text").get()
            quote_item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield quote_item

            # Збираємо посилання на авторів
            author_url = quote.css("span a::attr(href)").get()
            if author_url and quote_item["author"] not in self.authors:
                self.authors[quote_item["author"]] = response.urljoin(author_url)
                yield response.follow(author_url, callback=self.parse_author)

        # Переходимо на наступну сторінку
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author_item = AuthorItem()
        author_item["fullname"] = response.css("h3.author-title::text").get().strip()
        author_item["born_date"] = response.css("span.author-born-date::text").get()
        author_item["born_location"] = response.css("span.author-born-location::text").get()
        author_item["description"] = " ".join(response.css("div.author-description::text").getall()).strip()
        yield author_item
