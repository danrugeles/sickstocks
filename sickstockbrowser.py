import urllib2
from yahoofinance import *
from Transaction import *
from Peak import *
import re
import time

TOY=False
SPECIFIC=False
DEBUG=False


####REVIZAR OPXA AUg 7

if TOY:
	#**Variables
	PEAKDURATION=10
	PEAKINCREMENT=4
	INSURANCEINCREMENT=-0.2
	INSURANCEDURATION=7
	STABLEDURATION=20
	STABLEVAR=0.6
	STOPLIMIT=1.2
	EARNINGLIMIT=0.6
else:
	#**Variables
	PEAKDURATION=18
	PEAKINCREMENT=1.8
	INSURANCEINCREMENT=-0.2
	INSURANCEDURATION=18
	STABLEDURATION=20
	STABLEVAR=0.6
	STOPLIMIT=1.2
	EARNINGLIMIT=0.75
	VOLUMEMIN=0.7

found=["Symbol   Exchange   Peak_date    Peak_Per  Sell_date   Sell_price      Split"]

def printd(something):
	if DEBUG:
		print something
			
def searchPeaks(prices,duration,incr,shift):
	peaks=[]
	prices_aux=prices

	#If increment
	if incr>0:
		for t in range(len(prices_aux)):
			window=prices_aux[t:t+PEAKDURATION]
			printd(window)
			minimum = min(window)*1.0
			maximum = max(window[argmin(window):])*1.0
			start=argmin(window)+t
			stop=argmax(window[argmin(window):])+start
			percentage = (maximum-minimum)/minimum
			printd (percentage)
		
			if percentage >= PEAKINCREMENT:
				#Create peak
				if len(peaks)==0:
					peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
					printd("first_increment\n"+str(peaks[-1]))

				#Update peak if neccesary
				else:
					if ((start<=peaks[-1].stop and start>=peaks[-1].start) or (stop<=peaks[-1].stop and stop>=peaks[-1].start)):		
						#if (peaks[-1].percentage<percentage):	#Optimize for largest percentage
						peaks[-1].update(start+shift,stop+shift,minimum,maximum,percentage) 
						printd("update"+str(peaks[-1]))
					else:
						peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
						printd("create"+str(peaks[-1]))
			
	#if decrement peak
	else:
		for t in range(len(prices_aux)-INSURANCEDURATION+1):
			#print "decrement from ",t," until ",stop
			window=prices_aux[t:t+INSURANCEDURATION]
			printd(window)
	
			maximum = max(window)*1.0
			minimum = min(window[argmax(window):])*1.0
			start=argmax(window)+t
			stop=argmin(window[argmax(window):])+start
			percentage = (minimum-maximum)/maximum
			printd (percentage)
		
			if percentage <= INSURANCEINCREMENT:
				#Create peak
				if len(peaks)==0:
					peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
					printd("first_decrement\n"+str(peaks[-1]))
				
				#Update peak if neccesary
				else:
					if ((start<=peaks[-1].stop and start>=peaks[-1].start) or (stop<=peaks[-1].stop and stop>=peaks[-1].start)):		
						#if (peaks[-1].percentage<percentage):	#optimize for larger peaks
						peaks[-1].update(start+shift,stop+shift,minimum,maximum,percentage) 
						printd("update_decrement"+str(peaks[-1]))
					else:
						peaks.append(Peak(start+shift,stop+shift,minimum,maximum,percentage))
						printd("create_decrement"+str(peaks[-1]))
	return peaks
	
def searchStable(prices,variancemax):
	#return (var(prices)<variancemax)
	return (var(prices)<variancemax) and mean(prices)>=0.5 and mean(prices)<5

def getSickStocks(symbol,prices,dates,volume,exchange):
	peaks=searchPeaks(prices,PEAKDURATION,PEAKINCREMENT,0)
	for peak in peaks:
		if searchStable(prices[max(0,peak.start-STABLEDURATION):peak.start],STABLEVAR) and peak.stop>=len(prices)-INSURANCEDURATION and sum(volume!=0)*1.0/len(volume)>=VOLUMEMIN:
			printd("Stable, recent and volume condition accomplished")
			for idx,price in enumerate(prices[peak.stop:]):
				if price<peak.maximum*0.8:
					if checkSplit(symbol):
							found.append(symbol+"      "+exchange+"      "+dates[peak.stop]+"    "+"{0:.1f}".format(peak.percentage*100)+"%   "+dates[idx+peak.stop]+"   "+str(prices[idx+peak.stop])+" ("+str(peak.maximum*0.8)+")  split_warning")
					else:	
						found.append(symbol+"      "+exchange+"      "+dates[peak.stop]+"    "+"{0:.1f}".format(peak.percentage*100)+"%   "+dates[idx+peak.stop]+"   "+str(prices[idx+peak.stop])+" ("+str(peak.maximum*0.8)+")  No_split")
					return

			if checkSplit(symbol):
				found.append(symbol+"      "+exchange+"      "+dates[peak.stop]+"    "+"{0:.1f}".format(peak.percentage*100)+"%      None      "+str(prices[-1])+" ("+str(peak.maximum*0.8)+")  split_warning")
			else:	
				found.append(symbol+"      "+exchange+"      "+dates[peak.stop]+"    "+"{0:.1f}".format(peak.percentage*100)+"%      None      "+str(prices[-1])+" ("+str(peak.maximum*0.8)+")  No_split")


def writeResults(exchange):
	with open("Results_"+exchange+".csv","w") as w:
		for result in found:
			w.write(result+"\n")

def printResults():
	for result in found:
		print result
		
		
def getListAllStocks(i,exchange):
	#Override ONLINE
	#print "Warning: getListAllStocks from downloadStocks overrode 'ONLINE' variable to be false"
	if False:
		response = urllib2.urlopen('http://eoddata.com/stocklist/'+exchange+'/'+chr(i)+'.htm')
		html=response.read()
		response.close()
		allstocks=re.findall(r"(<A href=\"/stockquote/"+exchange+"/)(\w*)(.htm)",html)
		save("StockList/"+chr(i)+"_"+exchange,allstocks)
	else:
		allstocks=load("StockList/"+chr(i)+"_"+exchange+".npy")
	return allstocks



if __name__=="__main__":
	if TOY:
		prices=array([2,1,3,2,3,2,3,2,1,2,3,2,3,4,3,6,8,10,11,11,12,11,10,9,10,9,7,5,4,6,5,4,5,6,4,4,3,2,1,3,2,1,5,7,2,8])
		dates=ones(len(prices)).astype('str')
		getSickStocks("MOM",prices,"NASDAQ")
		getResults("NASDAQ")

	if not SPECIFIC:
		for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:#"NASDAQ","NYSE","OTCBB","AMEX"
			found=["Symbol   Exchange   Peak_date    Peak_Per  Sell_date   Sell_price      Split"]
			print exchange
			for i in xrange(65,91):#65,91
				print chr(i)
				
				allstocks=getListAllStocks(i,exchange)
			
				for stock in allstocks:
					symbol=stock[1]		
					done=False
					while not done:
						try:

							dates,prices,volume=getCurrentData(symbol)
							dates=dates[::-1]
							prices=prices[::-1]
							getSickStocks(symbol,prices,dates,volume,exchange)
							done=True
						except ValueError:
							done=True
							#print "Stock: "+symbol+" does not exist"
						except IOError:
							done=False
							print "Internet connection failed"
							time.sleep(30)		
			
			writeResults(exchange)	

		#CERE -- Too low peask
		#VPCO -- Too low peak
		#UQM -- Too low peak
		#SGOC -- Only buy do not sell yet
		#FMCC -- Negative march Positively- June
		#CLNT -- Disqualify not enough peaks
		#BIZM -- Not ready to sell
		#MCOX -- Not ready to sell	

# We need a filter for volume 0

	if SPECIFIC:		
		symbol="CDMHY"

		done=False
		while not done:
			try:
				dates,prices,volume=getCurrentData(symbol)
				dates=dates[::-1]
				prices=prices[::-1]
				
				getSickStocks(symbol,prices,dates,volume,"NYSE")
				done=True
			except ValueError:
				done=True
				#print "Stock: "+symbol+" does not exist"
			except IOError:
				done=False
				print "Internet connection failed"
				time.sleep(30)		

		printResults()	





