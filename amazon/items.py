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
        if 'New' in seller:
            try:
                return re.search('New \((.*)\) from ', seller).group(1)
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

    

#test = '<tr>\n<th class="a-color-secondary a-size-base prodDetSectionEntry">\nBest Sellers Rank\n</th>\n<td>\n<span>\n\n<span>#2,455 in Home &amp; Kitchen (<a href="/gp/bestsellers/home-garden/ref=pd_zg_ts_home-garden">See Top 100 in Home &amp; Kitchen</a>)</span>\n<br>\n\n<span>#12 in <a href="/gp/bestsellers/home-garden/3733671/ref=pd_zg_hrsr_home-garden">Home Office Desks</a></span>\n<br>\n\n</span>\n</td>\n</tr>'
#test = '<li><span class="a-list-item">\n\n\n\n<span class="a-text-bold">\nBest Sellers Rank:\n</span>\n#8 in <a href="/gp/bestsellers/pc/6795233011/ref=pd_zg_hrsr_pc">Lightning Cables</a>\n<ul class="a-unordered-list a-nostyle a-vertical zg_hrsr">\n\n</ul>\n\n\n\n</span></li>'
#t='<tr>\n<th class="a-color-secondary a-size-base prodDetSectionEntry">\nProduct Dimensions\n</th>\n\n<td class="a-size-base">\n67.1 x 47.3 x 29.5 inches\n</td>\n</tr>'
#print('Package Dimensions'  in t)
#print('Best Sellers' in test)
#t='asfasdfd'
#print(remove_tags(t))
#test = '<tr>\n<th class="a-color-secondary a-size-base prodDetSectionEntry">\nProduct Dimensions\n</th>\n\n<td class="a-size-base">\n39.37 x 23.62 x 29.53 inches\n</td>\n</tr>'
#print('Package Dimensions'  in AmazonItem.replacenewspace(test) or 'Product Dimensions'  in AmazonItem.replacenewspace(test) or 'inches' in AmazonItem.replacenewspace(test))
