import scrapy
from scrapy.loader  import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re
class AmazonItem(scrapy.Item):

    def addurl(value):
        return "https://www.amazon.com"+value

    def brandclean(brand):

        if 'Visit the ' in brand:
            return brand.replace('Visit the ',"").strip()
        elif 'Brand: ' in brand:
            return brand.replace('Brand: ',"").strip()
    def activeseller_clean(seller):
        try:
            return re.search('\((.*)\) from ', seller).group(1)
        except:
            return "1"
    
        return "1"

    def tr(value):
        
        return re.findall(r'#\d\d(.*)', value)

    def replacenewspace(value):
        return value.replace('\n',"").strip()
    def replacebestseller(value):
        return value.replace('Best Sellers Rank',"").strip()
    def replacebestseller2(value):
        return value.replace(':',"").strip()                 
    def getweight(value):
        return value.split(" inches; ")[1]
    def reaplacedimension(value):
        return value.replace('Package Dimensions:',"").strip()


    url = scrapy.Field(input_processor=MapCompose(addurl),output_processor = TakeFirst())
    img = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    reviews = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    brand = scrapy.Field(input_processor=MapCompose(remove_tags,brandclean),output_processor = TakeFirst())
    ASIN = scrapy.Field(output_processor = TakeFirst())
    weight = scrapy.Field(output_processor = TakeFirst())
    buybox = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    bestseller = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,replacebestseller,replacebestseller2),output_processor = TakeFirst())
    activeseller = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,activeseller_clean),output_processor = TakeFirst())
    Dimensions = scrapy.Field(output_processor = TakeFirst())
    firstdate = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace),output_processor = TakeFirst())

test = ''
#print(AmazonItem.replacenewspace(remove_tags(test)))
print(AmazonItem.activeseller_clean(AmazonItem.replacenewspace(remove_tags(test))))
