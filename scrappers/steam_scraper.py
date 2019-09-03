import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse
from . import HotTopicsSpider

class SteamSpider(HotTopicsSpider):
    name = "steam_games"
    output_file_name = 'steam_games.csv'

    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI': output_file_name
    }

    def parse(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        for list_element in response.xpath('//div[@id="NewReleasesTable"] // a[contains(@class, "tab_item")]'):
            title = list_element.xpath('div[@class="tab_item_content"] // div[@class="tab_item_name"]/text()').get()
            url = list_element.xpath('@href').get()
            yield {'topic': title, 'category': category, 'subcategory': subcategory, 'url': url}
            