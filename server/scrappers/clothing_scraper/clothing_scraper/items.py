# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ClothingItem(scrapy.Item):
    id = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    available_sizes = scrapy.Field()

