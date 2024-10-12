import scrapy
from scrapy.loader import ItemLoader
from  itemloaders.processors import TakeFirst
from ..items import JobItem


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = ['https://www.bayt.com/en/international/jobs/']
    
    base_url = "https://www.bayt.com"

    def parse(self, response):
        for i in response.xpath("//a[@data-js-aid='jobID']/@href").getall():
            yield scrapy.Request(
                url=self.base_url + i,
                callback=self.parse_job
            )

        for i in range(2, 501):
            yield scrapy.Request(
                url=f"https://www.bayt.com/en/international/jobs/?page={i}",
                callback=self.parse
            )

    def parse_job(self, response):
        loader = ItemLoader(JobItem(), response=response)
        loader.default_output_processor = TakeFirst()
        
        loader.add_xpath("title", "//h1/text()")
        loader.add_xpath("skills", "//h2[contains(text(), 'Skills')]/parent::node()")
        loader.add_xpath("skills", "//h2[contains(text(), 'Skills')]/following-sibling::p")
        loader.add_xpath("job_description", "//h2[contains(text(), 'Job Description')]/following-sibling::div")
        loader.add_xpath("job_location", "//dt[contains(text(), 'Job Location')]/following-sibling::dd/text()")
        loader.add_xpath("company_industry", "//dt[contains(text(), 'Company Industry')]/following-sibling::dd/text()")
        loader.add_xpath("company_type", "//dt[contains(text(), 'Company Type')]/following-sibling::dd/text()")
        loader.add_xpath("job_role", "//dt[contains(text(), 'Job Role')]/following-sibling::dd/text()")
        loader.add_xpath("employment_type", "//dt[contains(text(), 'Employment Type')]/following-sibling::dd/text()")
        loader.add_xpath("monthly_salary_range", "//dt[contains(text(), 'Monthly Salary Range')]/following-sibling::dd/text()")
        loader.add_xpath("number_of_vacancies", "//dt[contains(text(), 'Number of Vacancies')]/following-sibling::dd/text()")
        loader.add_xpath("career_level", "//dt[contains(text(), 'Career Level')]/following-sibling::dd/text()")
        loader.add_xpath("years_of_experience", "//dt[contains(text(), 'Years of Experience')]/following-sibling::dd/text()")

        yield loader.load_item()

