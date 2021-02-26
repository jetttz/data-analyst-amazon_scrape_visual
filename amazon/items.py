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
            return "0"
    
        return "0"

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
    def reaplacedimension2(value):
        return value.replace('Product Dimensions:',"").strip()        
    def cleanrating(value):
    	return value.replace(' out of 5 stars',"").strip()
    def cleandimension(value):
        return value.replace('inches',"").strip()
    def cleandollarsign(value):
        return value.replace('$','').replace(',','').strip()
    def reaplaceddatefirst(value):
        return value.replace('Date First Available:',"").strip()

    def cleanreviews(value):
        return value.replace(',','').replace(' ratings','').replace(' rating','').strip()
    def cleanreviews2(value):
        if 'Save' in value or 'save' in value:
            return '0'
        else:
            return value


    def cleanbestseller(value):
        return value.replace('amp;','').strip()

    def cleanbestseller2(value):
        try:
            return value.replace(re.findall(r"\(.*?\)", value)[0],'')    
        except:
            return value
    def ouncestolbs(value):
        

        if 'ounces' in value or 'ounce' in value or 'Ounces' in value:
            return float(value.replace('ounces','').replace('Ounces','').replace('ounce','')) * 0.0625
            
        return float(value.replace('Pounds','').replace('lbs','').replace('pounds',''))
    def cleanamazonbrand(value):
        if 'Amazon' in value or 'amazon' in value:
            return 'Amazon'
        return value
    def checkifnumber(value):
        if str(value).replace('.','').isdigit():
            return value
        return '0'
    def cleanna(value):
        return value.replace('N\A','n/a').replace('Store','').replace('store','').strip()
        
    url = scrapy.Field(input_processor=MapCompose(addurl), output_processor = TakeFirst())
    img = scrapy.Field(input_processor=MapCompose(remove_tags),output_processor = TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace),output_processor = TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags,cleanrating,checkifnumber),output_processor = TakeFirst())
    reviews = scrapy.Field(input_processor=MapCompose(remove_tags,cleanreviews,cleanreviews2,checkifnumber),output_processor = TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags,cleandollarsign,replacenewspace,checkifnumber),output_processor = TakeFirst())
    brand = scrapy.Field(input_processor=MapCompose(remove_tags,brandclean,cleanamazonbrand,cleanna),output_processor = TakeFirst())
    ASIN = scrapy.Field(output_processor = TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace),output_processor = TakeFirst())
    weight_lbs = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,ouncestolbs,checkifnumber),output_processor = TakeFirst())
    buybox = scrapy.Field(input_processor=MapCompose(remove_tags,cleanamazonbrand),output_processor = TakeFirst())
    bestseller = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,replacebestseller,replacebestseller2,cleanbestseller,cleanbestseller2),output_processor = TakeFirst())
    activeseller = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,activeseller_clean,checkifnumber),output_processor = TakeFirst())
    Dimensions = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,reaplacedimension,reaplacedimension2,cleandimension), output_processor = TakeFirst())
    firstdate = scrapy.Field(input_processor=MapCompose(remove_tags,replacenewspace,reaplaceddatefirst),output_processor = TakeFirst())