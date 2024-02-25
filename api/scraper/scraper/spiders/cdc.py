import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from scraper.scraper.link import LinkFinder
from scraper.scraper.items import ScraperItem

class CDCScraper(scrapy.Spider):
    
    urls = LinkFinder()
    name = "cdc"
    start_urls = urls.return_cdc_urls()
    allowed_domains = [url.replace("https://", "") for url in start_urls]

    def parse(self, response):
        loader = ItemLoader(item=ScraperItem(), response=response)

        # Assuming you have multiple matches for each type of HTML element
        diseases_html_list = response.xpath('//td[@class="other-clinician-disease"]/a').getall()
        health_report_html_list = response.xpath('//span[@class="summary"]').getall()
        vaccines_html_list = response.xpath('//td[@class="clinician-disease"]/a').getall()

        # Add concatenated HTML strings to the loader with the appropriate input processors
        loader.add_value('diseases', diseases_html_list)
        loader.add_value('health_report', health_report_html_list)
        loader.add_value('vaccines', vaccines_html_list)
        loader.add_value('name', response.url)

        # Load the item and yield it
        yield loader.load_item()

