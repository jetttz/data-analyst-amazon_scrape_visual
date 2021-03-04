from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import sys,psycopg2,os

from spiders import searchlist

class AmazonPipeline:
	
	def open_spider(self,spider):
		self.file = open(searchlist.searchquery.searchitem.replace(' ','_')+".csv", 'wb')
		self.exporter = CsvItemExporter(self.file)
		self.exporter.start_exporting()
		self.hostname = '192.168.1.185'
		self.username = 'pi'
		self.password = 'password'
		self.database='amazon'
		self.conn = psycopg2.connect(host = self.hostname,database=self.database,user=self.username, password=self.password, port = 5432)
		self.conn.autocommit = True
		self.cursor = self.conn.cursor()
		self.filename = searchlist.searchquery.searchitem.replace(' ','_')
		self.cursor.execute('DROP TABLE IF EXISTS {};'.format(self.filename))
		self.cursor.execute('CREATE TABLE {} (url TEXT,img TEXT,title TEXT,rating FLOAT,reviews FLOAT,price FLOAT,brand TEXT,ASIN  TEXT,description TEXT,weight_lbs  FLOAT,buybox TEXT,bestseller TEXT,activeseller FLOAT,Dimensions TEXT,firstdate TEXT);'.format(self.filename))

	def close_spider(self,spider):
		self.cursor.close()
		self.conn.close()
		self.exporter.finish_exporting()
		self.file.close()
		
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
		item.setdefault('weight_lbs','0')
		item.setdefault('buybox','n/a')
		item.setdefault('bestseller','n/a')
		item.setdefault('activeseller','0')
		item.setdefault('firstdate','n/a')
		item.setdefault('description','n/a')
		self.exporter.export_item(item)
		self.cursor.execute("insert into "+ self.filename + " (url,img,title,rating,reviews,price,brand,asin,description,weight_lbs,buybox,bestseller,activeseller,dimensions,firstdate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['url'],item['img'],item['title'],item['rating'],item['reviews'],item['price'],item['brand'],item['ASIN'],item['description'],item['weight_lbs'],item['buybox'],item['bestseller'],item['activeseller'],item['Dimensions'],item['firstdate']))
		return item


