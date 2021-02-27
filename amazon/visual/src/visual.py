import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_pdf import PdfPages
import sys,os
from sqlalchemy import create_engine
#import psycopg2

from amazon.visual import a

class visual:

	def __init__(self):
		self.engine = create_engine('postgresql://pi:maoping@192.168.1.185:5432/amazon')
		self.df = pd.read_sql_table('mouse_trap',self.engine)
		self.hostname = '192.168.1.185'
		self.username = 'pi'
		self.password = 'maoping'
		self.database='amazon'
		self.pp = PdfPages('multipage.pdf')

		self.conn = psycopg2.connect(host = self.hostname,database=self.database,user=self.username, password=self.password, port = 5432)
		self.conn.autocommit = True
		self.cursor = self.conn.cursor()
	

	def close_database(self):
		self.cursor.close()
		self.conn.close()
	

	def price_range(self):
		df = self.df.replace(0, np.NaN)
		mean = df['price'].mean()
		small_bins = [0.001,10,25,50,75,100,200,300]
		medium_bins = [0.001,50,100,150,200,250,300,400]
		big_bins = [0.001,100,250,500,750,1000,2000,3000]
		final_bins = []
		if mean <= 200:
			final_bins = small_bins
			above_price = [len(df.loc[df['price'] > 300])]
		elif mean > 300 and df['price'].mean() <= 500 :
			final_bins = medium_bins
			above_price = [len(df.loc[df['price'] > 400])]
		else:
			final_bins = big_bins
			above_price = [len(df.loc[df['price'] > 3000])]
			
		sizes = list(df['price'].value_counts(bins=final_bins).sort_index(ascending=True)) + above_price
		labels = ['Under $'+str(final_bins[1]),'\$'+str(final_bins[1])+' - \$' + str(final_bins[2]),'\$'+str(final_bins[2])+' - \$' + str(final_bins[3]),'$'+str(final_bins[3])+' - \$' + str(final_bins[4]),'$'+str(final_bins[4])+' - \$' + str(final_bins[5]),'\$'+str(final_bins[5])+' - \$' + str(final_bins[6]),'\$'+str(final_bins[6])+' - \$' + str(final_bins[7]),'\$'+str(final_bins[7])+' & Above']
		for index,val in enumerate(sizes):
			if val <=0:
				del sizes[index]
				del labels[index]
		
		for index,val in enumerate(sizes):
			labels[index] = labels[index] + ' (' + "{:.2%}".format(val/sum(sizes)) + ')'

		patches, texts = plt.pie(sizes, startangle=90)
		plt.legend(patches, labels, loc="best",fontsize=10)
		plt.title('Price Range\n\n Average Price: $' + str(np.around(mean, decimals=2)))
		plt.axis('equal')
		plt.tight_layout()
		#plt.savefig(self.pp, format='pdf')
		#return plt
	def clean_brand(self):
		df = self.df.replace('n/a',np.NaN)
		for holder in df['brand']:
			for index,values in enumerate(df['brand']):
				if str(holder).lower() in str(values).lower():
					df.at[index,'brand']= str(holder).upper()
		self.df = df.replace('NAN',np.NaN)

	def brand(self):
		self.clean_brand()
		df = self.df.replace('n/a',np.NaN)
		brand = dict(df['brand'].value_counts(ascending=False))			
		total_brand = sum(brand.values())
		top = 20
		try:
			sizes = list(brand.values())[:top]
			labels = list(brand.keys())[:top]
		except:
			sizes = brand.values()
			labels = brand.keys()
			top = len(brand.values())

		for index,val in enumerate(sizes):
			if val <=0:
				del sizes[index]
				del labels[index]

		for index,val in enumerate(sizes):
			labels[index] = labels[index] + ' (' + "{:.2%}".format(val/total_brand) + ')'
		
		patches, texts = plt.pie(sizes, startangle=90)
		plt.legend(patches, labels, loc="best",fontsize=10)
		plt.title('Top '+ str(top) +' brands\n\n Total # of brands: ' + str(len(brand)))
		plt.axis('equal')
		plt.tight_layout()
		#plt.savefig(self.pp, format='pdf')
		#self.pp.close()
		plt.show()








if __name__ == "__main__":
	obj = visual()
	#obj.price_range()
	#obj.brand()

