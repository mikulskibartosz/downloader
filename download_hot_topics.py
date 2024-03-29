import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapers import UrlWithCategories, SteamSpider, IMDbSpider
import os

parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-d", help="set the output directory")
args = parser.parse_args()

output_file_name = 'hot_topics.csv'
output_file_path = f"{args.directory}/{output_file_name}" if args.directory else output_file_name

if args.directory and not os.path.exists(args.directory):
    os.makedirs(args.directory)

steam_urls = [
    UrlWithCategories(url = 'https://store.steampowered.com/tags/en/Racing/', category = 'game', subcategory = 'racing'),
    UrlWithCategories(url = 'https://store.steampowered.com/tags/en/Simulation/', category = 'game', subcategory = 'simulation'),
    UrlWithCategories(url = 'https://store.steampowered.com/genre/Free%20to%20Play/', category = 'game', subcategory = 'free_to_play')
]

imdb_spider = [
    UrlWithCategories(url = 'https://www.imdb.com/search/title?genres=action&title_type=feature&explore=genres', category = 'movie', subcategory = 'action'),
    UrlWithCategories(url = 'https://www.imdb.com/search/title?genres=comedy&title_type=feature&explore=genres', category = 'movie', subcategory = 'comedy'),
    UrlWithCategories(url = 'https://www.imdb.com/search/title?genres=music&title_type=tv_series,mini_series&explore=genres', category = 'tv', subcategory = 'music')
]

process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            })
process.crawl(SteamSpider, urls_with_categories = steam_urls)
process.crawl(IMDbSpider, urls_with_categories = imdb_spider)
process.start()

with open(output_file_path, 'w') as output:
    skip_header = False
    for file in [SteamSpider.output_file_name, IMDbSpider.output_file_name]:
        for index, line in enumerate(open(file, 'r')):
            if index == 0 and skip_header:
                continue
            output.write(line)
        skip_header = True
        os.remove(file)
            

