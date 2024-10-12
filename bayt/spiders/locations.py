import scrapy
from scrapy.loader import ItemLoader
from  itemloaders.processors import TakeFirst
from ..items import LocationItem

class LocationsSpider(scrapy.Spider):
    name = "locations"
    start_urls = ["https://www.bayt.com/en/international/jobs/"]

    base_url = "https://www.bayt.com"

    def parse(self, response):
        for i in response.xpath("((//label[contains(text(), 'Country')]/following-sibling::div)[1]//ul)/li/a[not(contains(text(), 'All'))]/@href").getall():
            yield scrapy.Request(
                url=self.base_url + i,
                callback=self.parse_country,
                cb_kwargs={
                "url_str": i
                }
            )

    def parse_country(self, response, url_str):
        loader = ItemLoader(LocationItem(), response=response)
        loader.default_output_processor = TakeFirst()

        country = response.xpath("(//label[contains(text(), 'Country')]/following-sibling::div[1]//ul//a[contains(@href, '/en/international/jobs/')])[2]/parent::node()/text()").get()
        
        loader.add_value("country", country)
        loader.add_value("city", "")
        loader.add_value("url", response.url)

        yield loader.load_item()

        for i in response.xpath("((//label[contains(text(), 'City')]/following-sibling::div)[1]//ul)/li/a[not(contains(text(), 'All'))]/@href").getall():
            yield scrapy.Request(
                url=self.base_url + i,
                callback=self.parse_city,
                cb_kwargs={
                "country": country,
                "url_str": url_str,
                # "loader": loader
                }
            )

    def parse_city(self, response, country, url_str):
        loader = ItemLoader(LocationItem(), response=response)
        loader.default_output_processor = TakeFirst()

        city = response.xpath(f"((//label[contains(text(), 'City')]/following-sibling::div[1]//ul//a[contains(@href, '{url_str}')])[2]/parent::node()/text())[1]").get()
        
        loader.add_value("country", country)
        loader.add_value("city", city)
        loader.add_value("url", response.url)

        yield loader.load_item()
