import numpy as np
import sickStocks as ss
from yahoofinance import *
from Transaction import *
from Peak import *
import Date 




def forAllPeaks(histogram,symbol,highs,lows,prices,close,volume,dates):

	peaks=ss.searchPeaks(highs,lows,ss.PEAKDURATION,ss.PEAKINCREMENT,0)
	for peak in peaks:
		#print peak
		#print dates[-1],volume[-1]
		#print zip(dates[261:271],volume[261:271])

		
		#Filters:
		if lows[peak.start]>0.01 and dates[peak.start]!=dates[peak.stop]:
			start_split=getDate(dates,peak.start-5)
			stop_split=getDate(dates,peak.stop+5)
			SPLIT=False

			#if SPLITFILTER:
			#Don't filter out
			if False:
				try:
					splits=load("../../../../Splits/"+symbol+"_"+exchange+".npy")
				except IOError:
					splits=[] #Only CBMXW failed

				for split in splits:
					if laterThan(split,start_split) and laterThan(stop_split,split):
						SPLIT=True
						break
			
			if not SPLIT:
				if ss.searchStable(prices[peak.start-ss.STABLEDURATION:peak.start],ss.STABLEVAR):
					#print "Going up"
					wentDown(histogram,symbol,highs,lows,prices,close,volume,lows[peak.start],peak.stop,dates,peak.start)
					decrementpeaks=ss.searchPeaks(highs[peak.start:peak.stop],lows[peak.start:peak.stop],ss.INSURANCEDURATION,ss.INSURANCEINCREMENT,peak.start)
					for p in decrementpeaks:
						if (p.maximum-peak.minimum)/peak.minimum>=ss.PEAKINCREMENT:
							#print "Going down"
							wentDown(histogram,symbol,highs,lows,prices,close,volume,lows[peak.start],p.start,dates,peak.start)
		

#** How many stocks went down back to base?
def wentDown(histogram,symbol,highs,lows,prices,close,volume,peakstartprice,starttime,dates,peakstarted):
	#print symbol,"Peak Start",peakstartprice,dates[peakstarted],"Peak stop",dates[starttime],close[starttime],volume[starttime]
	for time in range(starttime,len(prices)):
	
		t=time-starttime
		
		
		if peakstartprice >= lows[t]:
			histogram[10]+=1
			#Two weeks
			if t<11:
				histogram[0]+=1			
			#One month
			elif t<22:
				histogram[1]+=1			
			#Two Months
			elif t<44:
				histogram[2]+=1						
			#Three months
			elif t<66:
				histogram[3]+=1						
			#Six Months
			elif t<132:
				histogram[4]+=1						
			#Eight months
			elif t<198:
				histogram[5]+=1						
			#Twelve months
			elif t<264:
				histogram[6]+=1						
			#Eighteen months
			elif t<398:
				histogram[7]+=1			
			#More than eighteen months			
			else:
				histogram[8]+=1	
			
			#print "went down",dates[t+starttime],"lasting ",t			
			return 	
	
	#print "Didn't go down"
	histogram[9]+=1
	histogram[10]+=1



	
if __name__=="__main__":
	histogram=np.zeros(11)

	for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:
		print exchange
		for i in xrange(65,91):#65,91
			allstocks=getListAllStocks(i,exchange)	
			for idx,stock in enumerate(allstocks):
				if stock[1]>="A" and stock[1]<="Z": #debug condition
					dates=array([])
					highs=array([])
					lows=array([])
					prices=array([])
					volume=array([])
					close=array([])

					for year in range(2000,2014):#2000,2014
						symbol=stock[1]
						#print symbol,exchange,year
						d,h,l,p,v,c=ss.getStock(symbol,exchange,year)
						
						firstday=Date.toDaniDate(str(year)+"-01-01")
						
						das=filter(lambda date: Date.laterThan(Date.toDaniDate(date[0]),firstday),zip(d,h,l,p,v,c))
						
						try:
							d,h,l,p,v,c=zip(*das)
						except ValueError:
							dum=0
										
						dates=hstack((dates,d))
						highs=hstack((highs,h))
						lows=hstack((lows,l))
						prices=hstack((prices,p))
						volume=hstack((volume,v))
						close=hstack((close,c))
					
				
					volume=volume.astype(float)
				
					
					
			
					#for a,b,c,d,e,f in zip(dates,highs,lows,prices,close,volume):
						#print	symbol,a,b,c,d,e,f
			
				
				
					forAllPeaks(histogram,symbol,highs,lows,prices,close,volume,dates)
				
					#print stock[1],histogram
						
	print histogram
