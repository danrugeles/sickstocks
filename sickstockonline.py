#!/usr/bin/env python
import mycsv
import numpy as np
import yahoofinance as db
import datetime
import myemail

__author__ = "Dan Rugeles"
__copyright__ = "Copyright 2014, SickStocks"
__credits__ = ["Dan Rugeles"]
__license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "Dan Rugeles"
__email__ = "danrugeles@gmail.com"
__status__ = "Production"


if __name__="__main__:
	
	insurance=0.97

	#1. Read Candidates for Peak Event
	candidates_peak=mycsv.getCol("Results2_OTCBB2.csv",[0,1,3])
	candidates_peak=np.asarray(candidates_peak[1:])

	while True:
		#2A. Search for Short candidate among candidates
		for c in candidates_peak:
			symbol=c[0]
			peakstartprice=c[1]
			dates,highs,lows,prices,volume = db.pullIntraDay(symbol)
	
			peakidx=np.argmax(prices)

			if prices[peakidx]/peakstartprice >= 2.2:			
				if prices[-1]<=peakstartprice*insurance:
					if not myemail.sentEmail(symbol,prices[peakidx]):
						myemail.sendEmail(symbol,prices[peakidx])
					
		time.sleep(2)		

	#print datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')
