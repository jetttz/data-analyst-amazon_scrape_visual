import scrapy
from scrapy.loader import ItemLoader
#from scrapy.crawler import CrawlerProcess
#from twisted.internet import reactor, defer
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.crawler import CrawlerProcess
from w3lib.html import remove_tags
#import sys
#sys.path.append('../')
from ..items import AmazonItem


class searchquery(scrapy.Spider):
	name = 'listing'
	count = 1
	start_urls =['https://www.amazon.com/s?k=pen']
	def replacenewspace(self,value):
		return value.replace('\n',"").strip()
	def reaplacedimension(self,value):
		return value.replace('Package Dimensions:',"").strip()
		
	def reaplacedimension2(self,value):
		return value.replace('Product Dimensions:',"").strip()

	def reaplaceddatefirst(self,value):
		return value.replace('Date First Available:',"").strip()				
	def getweight(self,value):
		return value.split(" inches; ")	
	
	def parse(self,response):
		for products in response.css('div.s-result-item.s-asin'):
			a = ItemLoader(item=AmazonItem(),selector=products)
			a.add_css('url','a.a-link-normal.a-text-normal::attr(href)')
			a.add_css('img','img::attr(src)')
			if len(response.css('span.a-size-base-plus.a-color-base.a-text-normal'))  > 1 :
				a.add_css('title','span.a-size-base-plus.a-color-base.a-text-normal')
			else:
				a.add_css('title','span.a-size-medium.a-color-base.a-text-normal')
			a.add_css('rating','span.a-icon-alt')
			a.add_css('reviews','span.a-size-base')
			a.add_css('price','span.a-offscreen')
			a.add_css('ASIN','div.s-result-item.s-asin::attr(data-asin)')
			yield scrapy.Request('https://www.amazon.com'+ products.css('a.a-link-normal.a-text-normal::attr(href)').get(), callback=self.parse_2, meta={'loader': a},)
			
			
			
	def parse_2(self,response):
		l = ItemLoader(item=AmazonItem(),selector=response, parent=response.meta['loader'])
		l.add_css('brand','a[id="bylineInfo"]')
		if len(response.css('span.tabular-buybox-text')) >0:
			l.add_css('buybox','span.tabular-buybox-text')
		else:
			l.add_css('buybox','a[id="sellerProfileTriggerId"]')
			
		l.add_xpath('activeseller','//*[@id="olp_feature_div"]/div[2]')
		
		if len(response.css('div.a-row.a-spacing-base').css('tr')) > 0:

			for infoss in response.css('div.a-row.a-spacing-base').css('tr'):
				c = ItemLoader(item=AmazonItem(),selector=infoss, parent=response.meta['loader'])

				if 'Item Weight' in self.replacenewspace(infoss.get()):
					c.add_value('weight',self.replacenewspace(remove_tags(infoss.css('td::text').get())))
				elif 'inches' in self.replacenewspace(infoss.get()) :
					c.add_value('Dimensions',self.replacenewspace(remove_tags(infoss.css('td::text').get())))
				elif 'Date First' in self.replacenewspace(infoss.get()):
					c.add_css('firstdate','td')
				elif 'Best Sellers' in self.replacenewspace(infoss.get()):
					c.add_value('bestseller',self.replacenewspace(remove_tags(infoss.get())))
			yield c.load_item()

		elif len(response.css('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list').css('li')) > 0:
			for info in response.css('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list').css('li'):

				d = ItemLoader(item=AmazonItem(),selector=info, parent=response.meta['loader'])
				if 'Ounces' in self.replacenewspace(info.get()):
					d.add_value('weight',self.replacenewspace(self.getweight(remove_tags(info.css('span').get()))[1]))
					d.add_value('Dimensions',self.reaplacedimension2(self.reaplacedimension(self.replacenewspace(self.getweight(remove_tags(info.css('span').get()))[0]))))
				elif 'Date First' in self.replacenewspace(info.get()):
					d.add_value('firstdate',self.reaplaceddatefirst(self.replacenewspace(remove_tags(info.get()))))

				elif 'Sellers' in self.replacenewspace(info.get()):
					d.add_value('bestseller',remove_tags(info.get()))
			yield d.load_item()

