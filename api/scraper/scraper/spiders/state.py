import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from scraper.scraper.link import LinkFinder
from scraper.scraper.items import ScraperItem

class StateScraper(scrapy.Spider):
    
    urls = LinkFinder()
    name = "state"
    start_urls = urls.return_state_urls()
    allowed_domains = [url.replace("https://", "") for url in start_urls]

    def parse(self, response):
        loader = ItemLoader(item=ScraperItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_xpath('travel_safety_report', '//div[@class="tsg-rwd-emergency-alert-text"]')
        loader.add_value('name', response.url)

        item = loader.load_item()
        yield item
