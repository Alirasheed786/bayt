from datetime import date
import scrapy
from scrapy.loader import ItemLoader
import scrapy.utils
from ..items import CompanyItem
from itemloaders.processors import TakeFirst
from scrapy.utils.response import open_in_browser


class CompanySpider(scrapy.Spider):
    name = "company"

    base_url = "https://www.bayt.com"
    start_urls = [
        "https://www.bayt.com/en/algeria/companies/",
        "https://www.bayt.com/en/bahrain/companies/",
        "https://www.bayt.com/en/egypt/companies/",
        "https://www.bayt.com/en/india/companies/",
        "https://www.bayt.com/en/iraq/companies/",
        "https://www.bayt.com/en/jordan/companies/",
        "https://www.bayt.com/en/kuwait/companies/",
        "https://www.bayt.com/en/lebanon/companies/",
        "https://www.bayt.com/en/libya/companies/",
        "https://www.bayt.com/en/morocco/companies/",
        "https://www.bayt.com/en/oman/companies/",
        "https://www.bayt.com/en/pakistan/companies/",
        "https://www.bayt.com/en/qatar/companies/",
        "https://www.bayt.com/en/saudi-arabia/companies/",
        "https://www.bayt.com/en/tunisia/companies/",
        "https://www.bayt.com/en/uae/companies/",
        "https://www.bayt.com/en/yemen/companies/"
    ]

    def parse(self, response):
        country = response.url.split("/")[-3]
        if country == "saudi-arabia":
            country = "Saudi Arabia"
        elif country == "uae":
            country = "United Arab Emirates"
        country = country.title()

        for link in response.xpath("//div[@class='card-content t-center-d media-m']//a/@href").getall():
            yield scrapy.Request(
                url=self.base_url + link,
                callback=self.parse_company,
                cb_kwargs={
                    "country": country
                }
            )

        next_page = response.xpath("//li[@class='pagination-next']/a/@href").get()
        if next_page:
            yield scrapy.Request(
                url=self.base_url + next_page,
                callback=self.parse
            )

    def parse_company(self, response, country):
        # open_in_browser(response)
        loader = ItemLoader(CompanyItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_xpath("company_name", "//h1/text()")
        loader.add_xpath("company_name", "//h4[@data-automation-id='companyName']/@title")
        loader.add_xpath("company_name", "(//h4)[2]/@title")
        loader.add_value("location", country)
        loader.add_xpath("company_size", "(//h4)[2]/a/text()")
        loader.add_xpath("company_size", "(//h1/following-sibling::p)[3]/text()")
        loader.add_xpath("company_size", "((//h4)[2]/parent::node()/ul/li/span)[position() = last()]/text()")
        loader.add_xpath("industry", "(//h1/following-sibling::p)[1]/text()")
        loader.add_xpath("industry", "//li[@data-automation-id='industry']/text()")
        loader.add_xpath("website", "//h1/following-sibling::a/@href")
        loader.add_xpath("description", "//h3/parent::node()/p/text()")
        loader.add_value("url", response.url)
        loader.add_value("last_refreshed", date.today())

        yield loader.load_item()
