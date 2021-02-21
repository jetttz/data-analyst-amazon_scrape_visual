# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import sys,psycopg2

class AmazonPipeline:
	def open_spider(self,spider):
		self.file = open("listing.csv", 'wb')
		self.exporter = CsvItemExporter(self.file)
		self.exporter.start_exporting()
		self.hostname = '192.168.1.185'
		self.username = 'pi'
		self.password = 'maoping'
		self.database='amazon'
		self.conn = psycopg2.connect(host = self.hostname,database=self.database,user=self.username, password=self.password, port = 5432)
		self.conn.autocommit = True
		self.cursor = self.conn.cursor()

	def close_spider(self,spider):
		self.cursor.close()
		self.conn.close()
		self.exporter.finish_exporting()
		self.file.close()

	'''
	def open_spider(self,spider):
		self.file = open("listing.csv", 'wb')
		
		self.exporter = CsvItemExporter(self.file)
		
		self.exporter.start_exporting()
		

	def close_spider(self,spider):
		self.exporter.finish_exporting()
		
		self.file.close()
		
	'''	
	def process_item(self,item,spider):
		item.setdefault('Dimensions','n/a')
		item.setdefault('url','n/a')
		item.setdefault('brand','n/a')
		item.setdefault('img','n/a')
		item.setdefault('title','n/a')
		item.setdefault('rating','0')
		item.setdefault('reviews','0')
		item.setdefault('price','0')
		item.setdefault('ASIN','n/a')
		item.setdefault('weight_lbs','n/a')
		item.setdefault('buybox','n/a')
		item.setdefault('bestseller','n/a')
		item.setdefault('activeseller','0')
		item.setdefault('firstdate','n/a')
		item.setdefault('description','n/a')
		#url = "INSERT INTO iphone_charger(url) VALUES ('%s')" % item['url']
		#self.cursor.execute("insert into iphone_charger(description) values(%s)",(item['description'],))
		#self.cursor.execute(url)
		self.cursor.execute("insert into iphone_charger(url,img,title,rating,reviews,price,brand,asin,description,weight_lbs,buybox,bestseller,activeseller,dimensions,firstdate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['url'],item['img'],item['title'],item['rating'],item['reviews'],item['price'],item['brand'],item['ASIN'],item['description'],item['weight_lbs'],item['buybox'],item['bestseller'],item['activeseller'],item['Dimensions'],item['firstdate']))
		self.exporter.export_item(item)

		return item


