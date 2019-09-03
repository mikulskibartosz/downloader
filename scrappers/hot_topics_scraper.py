import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse

class HotTopicsSpider(Spider):
    def __init__(self, urls_with_categories):
        self.urls_with_categories = urls_with_categories

    def start_requests(self):
        for page in self.urls_with_categories:
            yield scrapy.Request(
                url = page.url,
                callback = self.parse,
                meta = {'category': page.category, 'subcategory': page.subcategory}
            )            