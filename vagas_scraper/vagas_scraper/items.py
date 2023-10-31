# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def retirar_virgulas(value):
    if ',' in value:
        value = value.replace(',', ' -')
    return value

class VagasScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    Nome_da_Empresa = scrapy.Field(
        output_processor = TakeFirst()
    )
    
    Titulo_da_Vaga = scrapy.Field(
        output_processor = TakeFirst()
    )
    Localizacao = scrapy.Field(
        input_processor = MapCompose(retirar_virgulas),
        output_processor = TakeFirst()
    )
    
    Detalhes_Cargo = scrapy.Field(
        input_processor = MapCompose(retirar_virgulas),
        output_processor = Join('; ')
    )
