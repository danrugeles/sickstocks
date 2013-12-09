import urllib2
from yahoofinance import *
from Transaction import *
from Peak import *
from Date import *
import time
import numpy as np

DEBUG=False
ONLINE=False
 
peakdurations=[10,15,18,22]#18
peakincrements=[1.2,1.6,1.8,2.2]#1.8
insurancedurations=[8,10,15,19]#15
insuranceincrements=[-0.05,-0.12,-0.17,-0.25]#-0.2
stoplimits=[1.1,1.15,1.2,1.25,1.3]#1.2
earninglimits=[0.45,0.55,0.65,0.75,0.85]#0.75
splitfilter=[True,False]


peakdurations=[10]#18
peakincrements=[2.2]#1.8
insurancedurations=[8]#15
insuranceincrements=[-0.25]#-0.2
stoplimits=[1.1]#1.2
earninglimits=[0.55]#0.75
splitfilter=[True]


STABLEDURATION=20
STABLEVAR=0.6
VOLUMEMIN=0.7

def printd(something):
	if DEBUG:
		print something
		
def searchPeaks(highs,lows,duration,incr,shift):
	peaks=[]
	highs_aux=highs
	lows_aux=lows
	
	#If increment
	if incr>0:
		for t in range(len(highs_aux)):
			window_highs=highs_aux[t:t+PEAKDURATION]
			window_lows=lows_aux[t:t+PEAKDURATION]
			printd(window_highs)
			#printd(getDate(t))
			
			minimum = float(min(window_lows))*1.0
			maximum = float(max(window_highs[argmin(window_lows):]))*1.0
			start=argmin(window_lows)+t
			stop=argmax(window_highs[argmin(window_lows):])+start
			
			try:
				percentage = (maximum-minimum)/minimum
			except ZeroDivisionError:
				percentage=0

			printd(percentage)
		
			if percentage >= PEAKINCREMENT:
				
				#Create peak
				if len(peaks)==0:
					peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
					printd("first_increment\n"+str(peaks[-1]))

				#Update peak if neccesary
				else:
					if ((start+shift<=peaks[-1].stop and start+shift>=peaks[-1].start) or (stop+shift<=peaks[-1].stop and stop+shift>=peaks[-1].start)):		
						#if (peaks[-1].percentage<percentage):	#Optimize for largest percentage
						peaks[-1].update(start+shift,stop+shift,minimum,maximum,percentage) 
						printd("update"+str(peaks[-1]))
					else:
						peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
						printd("create"+str(peaks[-1]))
			
	#if decrement peak
	else:
		for t in range(len(highs_aux)-INSURANCEDURATION+1):
			#print "decrement from ",t," until ",stop
			window_highs=highs_aux[t:t+INSURANCEDURATION]
			window_lows=lows_aux[t:t+INSURANCEDURATION]
			printd(window_highs)
			#printd(getDate(t))
	
			maximum = max(window_highs)*1.0
			minimum = min(window_lows[argmax(window_highs):])*1.0
			start=argmax(window_highs)+t
			stop=argmin(window_lows[argmax(window_highs):])+start
			
			percentage = (minimum-maximum)/maximum
			printd(percentage)
		
			if percentage <= INSURANCEINCREMENT:
				#Create peak
				if len(peaks)==0:
					peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
					printd("first_decrement\n"+str(peaks[-1]))	
				#Update peak if neccesary
				else:
					if ((start+shift<=peaks[-1].stop and start+shift>=peaks[-1].start) or (stop+shift<=peaks[-1].stop and stop+shift>=peaks[-1].start)):		
						#if (peaks[-1].percentage<percentage):	#optimize for larger peaks
						peaks[-1].update(start+shift,stop+shift,minimum,maximum,percentage) 
						printd("update_decrement"+str(peaks[-1]))
					else:
						peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
						printd("create_decrement"+str(peaks[-1]))
	return peaks
	
def searchStable(prices,variancemax):
	return (var(asarray(prices))<variancemax) and mean(asarray(prices))>=0.5 and mean(asarray(prices))<5

def getTransactions(T,symbol,highs,lows,prices,volume,year,dates):
	#if symbol=="SRGZ": #and sum(volume!=0)*1.0/len(volume)>=VOLUMEMIN:
	peaks=searchPeaks(highs,lows,PEAKDURATION,PEAKINCREMENT,0)
	for peak in peaks:
		start_split=getDate(dates,peak.start-5)
		stop_split=getDate(dates,peak.stop+5)
		SPLIT=False
	
		if SPLITFILTER:
			try:
				splits=load("../../../../Splits/"+symbol+"_"+exchange+".npy")
			except IOError:
				splits=[] #Only CBMXW failed

			for split in splits:
				if laterThan(split,start_split) and laterThan(stop_split,split):
					SPLIT=True
					break
				
		if not SPLIT:
			if searchStable(prices[peak.start-STABLEDURATION:peak.start],STABLEVAR) :	
				printd("Stable, volume and Specific Split condition accomplished")
				#print "Peaks",peak.minimum,peak.maximum,peak.maximum*0.9
				T.executeTransaction(symbol,highs,lows,prices,volume,peak.stop,year)
				#print "inc",T.transaction_container,dates[peak.start],dates[peak.stop]
				decrementpeaks=searchPeaks(highs[peak.start:peak.stop],lows[peak.start:peak.stop],INSURANCEDURATION,INSURANCEINCREMENT,peak.start)
				for p in decrementpeaks:
					#print "decrements",p
					if (p.maximum-peak.minimum)/peak.minimum>=PEAKINCREMENT:
						#print "we roll",(p.maximum-peak.minimum)/peak.minimum, p.maximum
						#print "execute Transaction from",prices[p.start],prices[p.stop]	
						#print "dec Peaks",p.minimum,p.maximum,p.maximum*0.9,p.start,p.stop
						T.executeTransaction(symbol,highs,lows,prices,volume,p.start,year)
						#print "dec",T.transaction_container,prices[peak.start:peak.stop+1],prices[p.start:1+p.stop]
	
def getStockOnline(symbol,year):
	dates=[]
	highs=[]
	lows=[]
	prices=[]
	volume=[]
	done=False
	while not done:
		try:
			dates,highs,lows,prices,volume=parseToList(symbol,year)
			dates=dates[::-1]
			prices=prices[::-1]
			highs=highs[::-1]
			lows=lows[::-1]
			#huh? why? 
			#T.dates=dates
			
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
		[dates,highs,lows,prices,volume]=load("../../../../Stocks/"+symbol+"_"+exchange+"_"+str(year)+".npy")
	except IOError: 
		#Stock might be too new (exceptions: XTLB)
		prices=array([])
		highs=array([])
		lows=array([])
		volume=array([])
		dates=array([])
	try:
		prices=prices.astype(np.float)
		highs=highs.astype(np.float)
		lows=lows.astype(np.float)
		volume=volume.astype(np.float)
	except ValueError:
		#Crazy price values e.g. ARNH 2011
		prices=array([])
		highs=array([])
		lows=array([])
		volume=array([])
		dates=array([])	
	return dates,highs,lows,prices,volume


def getStock(symbol,exchange,year):
	if ONLINE:
		dates,highs,lows,prices,volume=getStockOnline(symbol,year)
		save("Stocks/"+symbol+"_"+exchange+"_"+str(year),[dates,highs,lows,prices,volume])
	else:
		dates,highs,lows,prices,volume=getStockOffline(symbol,exchange,year)
		
	return dates,highs,lows,prices,volume


def getListAllStocks(i,exchange):
	if ONLINE:
		response = urllib2.urlopen('http://eoddata.com/stocklist/'+exchange+'/'+chr(i)+'.htm')
		html=response.read()
		response.close()
		allstocks=re.findall(r"(<A href=\"/stockquote/"+exchange+"/)(\w*)(.htm)",html)
		save("StockList/"+chr(i)+"_"+exchange,allstocks)
	else:
		allstocks=load("StockList/"+chr(i)+"_"+exchange+".npy")
	return allstocks

if __name__=="__main__":
	for year in range(2012,2011,-1):#2013,1999,-1
		for PEAKDURATION in peakdurations:		
			global PEAKDURATION
			for PEAKINCREMENT in peakincrements:
				global PEAKINCREMENT
				for INSURANCEDURATION in insurancedurations:
					global INSURANCEDURATION
					if year<2015: #or PEAKINCREMENT > 1.2 and PEAKDURATION==18:
						print "Progress... ",year,PEAKDURATION,PEAKINCREMENT,INSURANCEDURATION
						for INSURANCEINCREMENT in insuranceincrements:
							global INSURANCEINCREMENT
							for SPLITFILTER in splitfilter:
								global SPLITFILTER
								for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:#"NASDAQ","NYSE","OTCBB","AMEX"	
									T=Transaction()
									T.INSURANCEINCREMENT=INSURANCEINCREMENT
									T.stoplimits=stoplimits
									T.earninglimits=earninglimits
									T.constructTransactionContainer()

									for i in xrange(66,67):#65,91
										allstocks=getListAllStocks(i,exchange)					
										for idx,stock in enumerate(allstocks):
											#print stock[1]
											if stock[1]=="BKESY": #debug condition
												symbol=stock[1]
												dates,highs,lows,prices,volume=getStock(symbol,exchange,year)
												#for a,b,c,d,e in zip(dates,highs,lows,prices,volume):
													#print a,b,c,d,e
												if size(dates)!=0:
													#else: Stock not found, Might be new(exceptions:XTLB)
													T.dates=dates
													getTransactions(T,symbol,highs,lows,prices,volume,year,dates)
									
									name=exchange+"_"+str(PEAKDURATION)+"_"+str(PEAKINCREMENT)+"_"+str(INSURANCEDURATION)+"_"+str(INSURANCEINCREMENT)+"_"+str(SPLITFILTER)	
									T.createReport(name,year)

