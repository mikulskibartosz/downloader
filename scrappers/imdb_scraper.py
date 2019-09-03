import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse

class IMDbSpider(Spider):
    name = "imdb_movies"
    output_file_name = 'imbd_movies.csv'

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

    def __get_absolute_url(self, response, relative_url):
        parsed_uri = urlparse(response.url)
        return '{uri.scheme}://{uri.netloc}{relative_url}'.format(uri = parsed_uri, relative_url = relative_url)

    def parse(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        for title_element in response.xpath('//div[@class="lister-list"] // div[contains(@class, "lister-item")] // div[@class="lister-item-content"] // h3[@class="lister-item-header"] / a'):
            title = title_element.xpath('text()').get()
            relative_url = title_element.xpath('@href').get()
            url = self.__get_absolute_url(response, relative_url)
            yield {'topic': title, 'category': category, 'subcategory': subcategory, 'url': url}

            