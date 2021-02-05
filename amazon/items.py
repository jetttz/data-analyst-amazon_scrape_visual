import scrapy
from scrapy.loader  import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def addurl(value):
        return "https://www.amazon.com"+value

    url = scrapy.Field(input_processor=MapCompose(addurl),output_processor = TakeFirst())
    img = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    reviews = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    brand = scrapy.Field(output_processor = TakeFirst())
    buybox = scrapy.Field(output_processor = TakeFirst())
    category = scrapy.Field(output_processor = TakeFirst())
    activeseller = scrapy.Field(output_processor = TakeFirst())
    ASIN = scrapy.Field(output_processor = TakeFirst())
