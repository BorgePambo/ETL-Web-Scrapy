# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ColetaItem(scrapy.Item):
    #name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    old_price = scrapy.Field()
    old_price_cent = scrapy.Field()
    new_price = scrapy.Field()
    new_price_cent = scrapy.Field()
    review_number = scrapy.Field()
    review_amount = scrapy.Field()
