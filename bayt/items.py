# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import replace_escape_chars, remove_tags
from itemloaders.processors import MapCompose, Join


def replace_escape_chars_unicode(value):
    return replace_escape_chars(value, which_ones=("\n", "\t", "\r", "\xa0"))

def clean_skills(value):
    return replace_escape_chars(value, which_ones=("\n", "\t", "\r", "\xa0", "Skills"))

class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    location = scrapy.Field()
    company_size = scrapy.Field()
    industry = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    last_refreshed = scrapy.Field()


class LocationItem(scrapy.Item):
    country = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars_unicode)
    )
    city = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars_unicode)
    )
    # area = scrapy.Field()
    url = scrapy.Field()


class JobItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars_unicode)
    )
    skills = scrapy.Field(
        input_processor=MapCompose(clean_skills, remove_tags),
        output_processor=Join()
    )
    job_description = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars_unicode, remove_tags)
    )
    job_location = scrapy.Field()
    company_industry = scrapy.Field()
    company_type = scrapy.Field()
    job_role = scrapy.Field()
    employment_type = scrapy.Field()
    monthly_salary_range = scrapy.Field()
    number_of_vacancies = scrapy.Field()
    career_level = scrapy.Field()
    years_of_experience = scrapy.Field()
