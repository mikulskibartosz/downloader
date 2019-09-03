import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse

class SteamSpider(Spider):
    name = "steam_games"
    output_file_name = 'steam_games.csv'

    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI': output_file_name
    }
    
    def __init__(self, urls_with_categories):
        self.urls_with_categories = urls_with_categories

    def start_requests(self):
        for page in self.urls_with_categories:
            yield scrapy.Request(
                url = page.url,
                callback = self.parse,
                meta = {'category': page.category, 'subcategory': page.subcategory}
            )

    def parse(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        for list_element in response.xpath('//div[@id="NewReleasesTable"] // a[contains(@class, "tab_item")]'):
            title = list_element.xpath('div[@class="tab_item_content"] // div[@class="tab_item_name"]/text()').get()
            url = list_element.xpath('@href').get()
            yield {'topic': title, 'category': category, 'subcategory': subcategory, 'url': url}
            