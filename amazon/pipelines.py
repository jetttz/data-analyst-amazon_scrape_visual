# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class AmazonPipeline:
	def open_spider(self,spider):
		self.file = open("listing.csv", 'wb')
		
		self.exporter = CsvItemExporter(self.file)
		
		self.exporter.start_exporting()
		

	def close_spider(self,spider):
		self.exporter.finish_exporting()
		
		self.file.close()
		
		
	def process_item(self,item,spider):
		item.setdefault('Dimensions','n/a')
		item.setdefault('url','n/a')
		item.setdefault('img','n/a')
		item.setdefault('title','n/a')
		item.setdefault('rating','n/a')
		item.setdefault('reviews','n/a')
		item.setdefault('price','n/a')
		item.setdefault('ASIN','n/a')
		item.setdefault('weight','n/a')
		item.setdefault('buybox','n/a')
		item.setdefault('bestseller','n/a')
		item.setdefault('activeseller','n/a')
		item.setdefault('firstdate','n/a')
		item.setdefault('description','n/a')
		


		
		self.exporter.export_item(item)

		return item
