import scrapy
from scrapy.loader import ItemLoader
#from scrapy.crawler import CrawlerProcess
#from twisted.internet import reactor, defer
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.crawler import CrawlerProcess

#import sys
#sys.path.append('../')
from ..items import AmazonItem


class searchquery(scrapy.Spider):
	name = 'listing'
	start_urls =['https://www.amazon.com/s?k=iPhone+charger']

    
    	

	def parse(self,response):
		for products in response.css('div.s-result-item.s-asin'):
			l = ItemLoader(item=AmazonItem(),selector=products)
			l.add_css('url','a.a-link-normal.a-text-normal::attr(href)')
			l.add_css('img','img::attr(src)')
			l.add_css('title','span.a-size-medium.a-color-base.a-text-normal')
			l.add_css('rating','span.a-icon-alt')
			l.add_css('reviews','span.a-size-base')
			l.add_css('price','span.a-offscreen')
			l.add_css('ASIN','div.s-result-item.s-asin::attr(data-asin)')
			next_page = 'https://www.amazon.com'+ products.css('a.a-link-normal.a-text-normal::attr(href)').get()
			yield scrapy.Request(next_page, callback=self.parse_2, meta={'loader': l},)
			
	def parse_2(self,response):
		loader = response.meta['loader']
		l = ItemLoader(item=AmazonItem(),selector=response, parent=loader)
		l.add_css('brand','a[id="bylineInfo"]::text')
		yield l.load_item()


		
