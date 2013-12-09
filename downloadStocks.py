import urllib2
from yahoofinance import *
from Transaction import *
from Peak import *
from Date import *
import time
import numpy as np
from variables import *

def getStockOnline(symbol,year):
	dates=[]
	highs=[]
	lows=[]
	prices=[]
	volume=[]
	done=False
	while not done:
		try:
			dates,highs,lows,prices,volume=parseToList_yahoo(symbol,year)
			done=True
		except ValueError:
			done=True
			#print "Stock: "+symbol+" does not exist"
		except IOError:
			print "Internet connection failed"
			time.sleep(30)
		except UnboundLocalError:
			done=True

	return dates,highs,lows,prices,volume

def getStockOffline(symbol,exchange,year):
	try:
		[dates,highs,lows,prices,volume]=load("Stocks/"+symbol+"_"+exchange+"_"+str(year)+".npy")
	except IOError: 
		#Stock might be too new (exceptions: XTLB)
		prices=array([])
		highs=array([])
		lows=array([])
		volume=array([])
		dates=array([])
	prices=prices.astype(np.float)
	highs=highs.astype(np.float)
	lows=lows.astype(np.float)
	volume=volume.astype(np.float)
	return dates,highs,lows,prices,volume

def getListAllStocks(i,exchange):
	#Override ONLINE
	print "Warning: getListAllStocks from downloadStocks overrode 'ONLINE' variable to be false"
	if False:
		response = urllib2.urlopen('http://eoddata.com/stocklist/'+exchange+'/'+chr(i)+'.htm')
		html=response.read()
		response.close()
		allstocks=re.findall(r"(<A href=\"/stockquote/"+exchange+"/)(\w*)(.htm)",html)
		save("StockList/"+chr(i)+"_"+exchange,allstocks)
	else:
		allstocks=load("StockList/"+chr(i)+"_"+exchange+".npy")
	return allstocks


def getStock(symbol,exchange,year):
	if ONLINE:
		dates,highs,lows,prices,volume=getStockOnline(symbol,year)
		#save("Stocks/"+symbol+"_"+exchange+"_"+str(year),[dates,highs,lows,prices,volume])
		save("../../../../Stocks/"+symbol+"_"+exchange+"_"+str(year),[dates,highs,lows,prices,volume])
	else:
		dates,highs,lows,prices,volume=getStockOffline(symbol,exchange,year)
		
	return dates,highs,lows,prices,volume
	
if __name__=="__main__":
	for year in range(2004,1999,-1):#2013,1999,-1
		for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:#"NASDAQ","NYSE","OTCBB","AMEX"	
			for i in xrange(65,91):#65,91# nasdaq desde el 73
				allstocks=getListAllStocks(i,exchange)					
				print year,exchange,chr(i)
				for idx,stock in enumerate(allstocks):
					symbol=stock[1]
					#getStock(symbol,exchange,year)
					if year==2004 and exchange=="AMEX" and symbol >"EFNL":		
						getStock(symbol,exchange,year)
					#elif year==2009 and (exchange=="AMEX" or exchange =="OTCBB"):
						#getStock(symbol,exchange,year)
					elif year<2004:
						getStock(symbol,exchange,year)
