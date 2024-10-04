# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def cut_comma(value):
    if ',' in value:
        value = value.replace(',', ' -')
    return value

class VagasScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    Company_Name = scrapy.Field(
        output_processor = TakeFirst()
    )
    
    Job_Title = scrapy.Field(
        output_processor = TakeFirst()
    )
    Location = scrapy.Field(
        input_processor = MapCompose(cut_comma),
        output_processor = TakeFirst()
    )
