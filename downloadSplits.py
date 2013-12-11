from yahoofinance import *
import urllib2
import time
import downloadStocks as download

if __name__=="__main__":

	print "downloadSplits.py \nVersion 1.24 by Jaime Zalamea and Daniel Rugeles. December 2013"
	
	for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:#"NASDAQ","NYSE","OTCBB","AMEX"
		found=["Symbol   Exchange   Peak_date    Peak_Per  Sell_date   Sell_price      Split"]
		for i in xrange(65,91):#65,91
			print exchange,chr(i)
			allstocks=download.getListAllStocks(i,exchange)	

			for stock in allstocks:
				symbol=stock[1]		
				done=False
				while not done:
					try:
						#Only get splits from 2000
						splits=getSplitFast(symbol)
						#Deprecated function
						#splits=getSplitTime(symbol,[0,1,2012],[6,7,2013])
						#print "splits",splits	
						save("../../../../Splits/"+symbol+"_"+exchange,splits)
						#save("Splits/"+symbol+"_"+exchange,splits)
						done=True
					except ValueError:
						done=True
						print "Stock: "+symbol+" does not exist"
					except IOError:
						done=False
						print "IOError: Internet connection failed"
						time.sleep(5)									
