import urllib
import urllib2
from numpy import *
import datetime as dt
from Date import *
import re


#Data check. 
#Yahoo data had volume turned around!
#Yahoo data was not normalized
#Google data was not shifted
#Google data had lots of gaps when volume is 0

DEBUG=False

def checkSplit(symbol):
	#if stop-start > 50:
	#else:
	now=dt.datetime.now()
	
	try:
		#url = "http://finance.yahoo.com/q/hp?s="+symbol+"&a=10&b=1&c=2012&d=11&e=27&f=2012&g=d"
		if now.month-5<0:
			url = "http://finance.yahoo.com/q/hp?s="+symbol+"&a="+str((now.month-5)%12)+"&b="+str(now.day)+"&c="+str(now.year-1)+"&g=d"
		else:
			url = "http://finance.yahoo.com/q/hp?s="+symbol+"&a="+str((now.month-5)%12)+"&b="+str(now.day)+"&c="+str(now.year)+"&g=d"
		response=urllib.urlopen(url)
		html= response.read()
		match=re.search(r"Stock Split",html)
		if match:
			return True
		else:
			return False
	
	except urllib.ContentTooShortError as e:
		print e


def checkSplitTime(symbol,start,stop):
	#numMonths=getMonthDiff(start,stop)
	start_aux=start
	stop_aux=getNextStop(start)		

	while laterThan(stop,stop_aux):
		stop_aux=getNextStop(start_aux)		
		try:
			base_url="http://finance.yahoo.com/q/hp?s="		
			url = base_url+symbol+"&d="+str(stop_aux[0])+"&e="+str(stop_aux[1])+"&f="+str(stop_aux[2])+"&a="+str(start_aux[0])+"&b="+str(start_aux[1])+"&c="+str(start_aux[2])+"&g=d"

			response=urllib.urlopen(url)
			html= response.read()
			match=re.search(r"Stock Split",html)
			if match:
				return True
		
		except urllib.ContentTooShortError as e:
			print e
		start_aux=stop_aux
	return False


def getSplitFast(symbol):
	splits=[]
	try:
		base_url="http://ichart.finance.yahoo.com/x?s="
		url = base_url+symbol+"&a=00&b=1&c=2000&g=v&y=0&z=30000"	
		response=urllib.urlopen(url)
		html= response.read()
		html=html.strip("\n").split("\n")
		for line in html:
			column=line.split(",")
			if column[0]=="SPLIT":
				#Column one has the year
				#Column two has the split ratio
				splits.append(yyyymmddToDaniDate(column[1]))
		splits=array(splits)
		return splits[::-1]
		
	except urllib.ContentTooShortError as e:
		print e


def getSplitTime(symbol,start,stop):
	#numMonths=getMonthDiff(start,stop)
	start_aux=start
	stop_aux=getNextStop(start)		

	splits=[]
	while laterThan(stop,stop_aux):
		stop_aux=getNextStop(start_aux)		
		try:
			base_url="http://finance.yahoo.com/q/hp?s="		
			url = base_url+symbol+"&d="+str(stop_aux[0])+"&e="+str(stop_aux[1])+"&f="+str(stop_aux[2])+"&a="+str(start_aux[0])+"&b="+str(start_aux[1])+"&c="+str(start_aux[2])+"&g=d"
			print url
			response=urllib.urlopen(url)
			html= response.read()
			match=re.findall(r"(\w\w\w) (\w{1,2}), (\w\w\w\w)</([\w\s<>:\"=]*) (Stock Split)",html)

			for m in match:
					day=int(m[1])
					year=int(m[2])
					if m[0] =="Jan":
						month=0
					elif m[0]=="Feb":
						month=1
					elif m[0]== "Mar":
						month=2
					elif m[0]== "Apr":
						month=3
					elif m[0]== "May":
						month=4
					elif m[0]== "Jun":
						month=5
					elif m[0]== "Jul":
						month=6
					elif m[0]== "Aug":
						month=7
					elif m[0]== "Sep":
						month=8
					elif m[0]== "Oct":
						month=9
					elif m[0]== "Nov":
						month=10
					elif m[0]== "Dec":
						month=11
					splits.append([month,day,year])
	
		except urllib.ContentTooShortError as e:
			print e
		start_aux=stop_aux

	return splits


def cast2danidate(olddate):
	month= olddate[:3]

	if olddate[5]==",":
		day="0"+olddate[4:5]
		year=olddate[7:]
	else:
		day=olddate[4:6]
		year=olddate[8:]

	if month=="Jan":
		month="01"
	elif month=="Feb":
		month="02"
	elif month== "Mar":
		month="03"
	elif month== "Apr":
		month="04"
	elif month== "May":
		month="05"
	elif month== "Jun":
		month="06"
	elif month== "Jul":
		month="07"
	elif month== "Aug":
		month="08"
	elif month== "Sep":
		month="09"
	elif month== "Oct":
		month="10"
	elif month== "Nov":
		month="11"
	elif month== "Dec":
		month="12"
	else: 
		print "ERROR: month not specified! ",month

	newdate=year+"-"+month+"-"+day
	
	return newdate


#Get_Current_Data
def getCurrentData(symbol):
	#Number of months (int)
	window_size=2
	
	now=dt.datetime.now()
	base_url = "http://ichart.finance.yahoo.com/table.csv?s="
	
	try:
		if now.month-window_size<0:
			url=base_url + symbol + "&a="+str((now.month-window_size)%12)+"&b="+str(now.day)+"&c="+str(now.year-1)
		else:
			url=base_url + symbol + "&a="+str((now.month-window_size)%12)+"&b="+str(now.day)+"&c="+str(now.year)

		response=urllib.urlopen(url)
		html = response.read()	

		allinfo=html.strip("\n").split("\n")

		dates=[]
		highs=[]
		lows=[]
		volume=[]
		closes=[]
		prices=[]

		for idx,info in enumerate(allinfo):
			
			if idx>0:
				#Date,Open,High,Low,Close,Volume,Adj Close	
				d,o,h,l,c,v,ac=info.split(',')		

				#** Adjust High and low prices
				ac=float(ac)
				c=float(c)
				try: 	
					adj=ac/c
					closes.append(c)
					prices.append(ac)
					highs.append(float(h)*adj)
					lows.append(float(l)*adj)
					volume.append(v)
				except ZeroDivisionError:
					closes.append(0.0)
					prices.append(0.0)
					highs.append(0.0)
					lows.append(0.0)
					volume.append(0.0)
		
				dates.append(d)
		
		closes=array(closes)		
		prices=array(prices)
		highs=array(highs)
		lows=array(lows)
		volume=array(volume)
		volume=volume.astype(float)

		dates=dates[::-1]
		closes=closes[::-1]
		prices=prices[::-1]
		highs=highs[::-1]
		lows=lows[::-1]
		volume=volume[::-1]

		return dates,highs,lows,volume		
	
	except urllib.ContentTooShortError as e:
		print e


# YAHOO --------------------------/
# YAHOO  -------------------------\
#-YAHOO --------------------------/

def pullData_yahoo(symbol,year):
	base_url = "http://ichart.finance.yahoo.com/table.csv?s="
	try:
		url=base_url + symbol + "&d=11&e=31&f="+str(year)+"&g=d&a=10&b=1&c="+str(year-1)
		response=urllib.urlopen(url)
		return response.read()

	except urllib.ContentTooShortError as e:
		print e


#Data Retrieved is fixed
def parseToList_yahoo(symbol,year):
	html=pullData_yahoo(symbol,year)

	allinfo=html.strip("\n").split("\n")

	dates=[]
	closes=[]
	prices=[]
	highs=[]
	lows=[]
	volume=[]

	for idx,info in enumerate(allinfo):

		if idx>0:
			#Date,Open,High,Low,Close,Volume,Adj Close	
			d,o,h,l,c,v,ac=info.split(',')		
	
			#** Adjust High and low prices
			ac=float(ac)
			c=float(c)
			try: 	
				adj=ac/c
				closes.append(c)
				prices.append(ac)
				highs.append(float(h)*adj)
				lows.append(float(l)*adj)
				volume.append(v)
			except ZeroDivisionError:
				closes.append(0.0)
				prices.append(0.0)
				highs.append(0.0)
				lows.append(0.0)
				volume.append(0.0)
			
			dates.append(d)
			
	closes=array(closes)		
	prices=array(prices)
	highs=array(highs)
	lows=array(lows)
	volume=array(volume)
	volume=volume.astype(float)

	dates=dates[::-1]
	closes=closes[::-1]
	prices=prices[::-1]
	highs=highs[::-1]
	lows=lows[::-1]
	volume=volume[::-1]
	
	return dates,highs,lows,prices,volume,closes
	
	

# GOOGLE --------------------------/
# GOOGLE  -------------------------\
# GOOGLE --------------------------/

def pullIntraDay(symbol):
	url="http://www.google.com/finance/getprices?q="+symbol+"&i=60&p=1d&f=d,h,l,c,v"
	response=urllib.urlopen(url)
	html= response.read()	
	return parseGoogleIntradayData(html)
	


def pullData_google(symbol,year,start):
	url="https://www.google.com/finance/historical?q="+symbol+"&startdate=Dec+1%2C+"+str(year-1)+"&enddate=Dec+31%2C+"+str(year)+"&num=200&start="+str(start)
	response=urllib.urlopen(url)
	html= response.read()
	
	match=re.search("The requested URL was not found on this server.",html)
	if match:
		match=re.search("(\w*):"+symbol,html)
		if match:
			#** Check if symbol belongs to otcbb or otcmkts
			trade=match.group(1)		
			url="https://www.google.com/finance/historical?q="+trade+"%3A"+symbol+"&startdate=Dec+1%2C+"+str(year-1)+"&enddate=Dec+31%2C+"+str(year)+"&num=370"	
			response=urllib.urlopen(url)
			html= response.read()
		else:
			#print "ERROR URL "+url+" was not found and market was not found either!!!"
			with open("List_non_found_stocks_google.txt","a")as w:
				w.writelines(symbol+"\n")

	
	results=re.findall(r"(<td class=\"[rgtlm]+\s*[rm]*\">)([^\n^<^>^/^;^:^\"^&]*)",html)
	return results


#Pull data from Google finance
def parseToList_google(symbol,year):

	tries=0
	PULLING=True
	while PULLING:
		try:
			#** Pull all data from google
			results=pullData_google(symbol,year,start=0)
			dates,highs,lows,prices,volume=parseGoogleData(results)

			#** Check if server failed or data unavailable
			dummy=dates[-1]
			PULLING=False
		except IndexError:
			print "Try #",tries
			tries+=1	
			#** If no return after 2 trials assume data is unavailable.
			if tries>=2:
				return dates,highs,lows,prices,volume

	#** Check if we need to pull more data from google for same stock
	if (laterThan(toDaniDate(dates[-1]),[11,15,year-1])):
		results=pullData_google(symbol,year,start=200)
		dates2,highs2,lows2,prices2,volume2=parseGoogleData(results)

		#** Check if there exists duplicate data
		if laterThan(toDaniDate(dates[-1]),toDaniDate(dates2[0])):
			dates=hstack((dates2,dates))
			volume=hstack((volume2,volume))
			highs=hstack((highs2,highs))
			lows=hstack((lows2,lows))
			prices=hstack((prices2,prices))
			
	return dates,highs,lows,prices,volume

def parseGoogleIntradayData(htmlresponse):
	prices=[]
	highs=[]
	lows=[]
	volume=[]
	dates=[]

	htmlresponse=htmlresponse.strip("\n").split("\n")
	
	for idx,m in enumerate(htmlresponse):
		stream=m.split(",")
		if idx==7:
			t_init=int(stream[0].lstrip("a"))
			dates.append(t_init)
			highs.append(float(stream[1]))
			lows.append(float(stream[2]))
			prices.append(float(stream[3]))
			volume.append(float(stream[4]))
			
		if idx>7:
			dates.append(int(stream[0])+t_init)
			highs.append(float(stream[1]))
			lows.append(float(stream[2]))
			prices.append(float(stream[3]))
			volume.append(float(stream[4]))
	
	try:
		prices=asarray(prices).astype(float)
		highs=asarray(highs).astype(float)
		lows=array(lows).astype(float)
		

	except ValueError:	#Fail in stocks with price greater than 1000 like GOOG 2013
		prices=array([re.sub(",","",price) for price in prices])
		prices=prices.astype(float)

		highs=array([re.sub(",","",high) for high in highs])
		prices=highs.astype(float)

		lows=array([re.sub(",","",low) for low in lows])
		lows=lows.astype(float)

	volume=array(volume)
	volume=volume.astype(float)

	#dates=dates[::-1]
	#prices=prices[::-1]
	#highs=highs[::-1]
	#lows=lows[::-1]
	#volume=volume[::-1]

	# the last prices overwrites the original close price not provided by google
	return dates,highs,lows,prices,volume


def parseGoogleData(htmlresponse):
	prices=[]
	highs=[]
	lows=[]
	volume=[]
	dates=[]
	deletelastrow=False
	updatehighlow=False

	for idx,m in enumerate(htmlresponse):
		#print m
		#Date
		if idx%6==0:
			#Unavailable data  e.g. Nov 27,2008 AAPL
			if m[1]=="-":
				deletelastrow=True
			else:
				deletelastrow=False
				
			newdate=cast2danidate(m[1])
			dates.append(newdate)
	
		#High
		if idx%6==2:
			if m[1]=="-":
				updatehighlow=True
			highs.append(m[1])
	
		#Low
		if idx%6==3:
			if m[1]=="-":
				updatehighlow=True
			lows.append(m[1])
	
		#Close
		if idx%6==4:
			if m[1]=="-" or deletelastrow:
				deletelastrow=True
			else:
				#deletelastrow is definitvely false otherwise the if would have been activated
				if updatehighlow:
					del highs[-1]
					del lows[-1]
					lows.append(m[1])
					highs.append(m[1])
					
			prices.append(m[1])
		
		#Volume
		if idx%6==5:	
			if m[1]=="-":
				deletelastrow=True
			volume.append(m[1].replace(",",""))
		
			#UIHC from 2008 is lacking a lot of stock data 
			if deletelastrow:
				try:
					del volume[-1]
					del prices[-1]
					del highs[-1]
					del lows[-1]
					del dates[-1]
				except IndexError:
					print "check for '-' data because it called del volume [-1]!!!!",symbol,year
	
	try:
		prices=array(prices)
		prices=prices.astype(float)
					
		highs=array(highs)
		highs=highs.astype(float)
		
		lows=array(lows)
		lows=lows.astype(float)
	
	except ValueError:	#Fail in stocks with price greater than 1000 like GOOG 2013
		prices=array([re.sub(",","",price) for price in prices])
		prices=prices.astype(float)
	
		highs=array([re.sub(",","",high) for high in highs])
		prices=highs.astype(float)

		lows=array([re.sub(",","",low) for low in lows])
		lows=lows.astype(float)

	volume=array(volume)
	volume=volume.astype(float)

	dates=dates[::-1]
	prices=prices[::-1]
	highs=highs[::-1]
	lows=lows[::-1]
	volume=volume[::-1]
	# the last prices overwrites the original close price not provided by google
	return dates,highs,lows,prices,volume,prices

#* Mix of Yahoo and Google EOD Data
def parseToList(symbol,year):

	d_google,h_google,l_google,p_google,v_google=parseToList_google(symbol,year)
	d_yahoo,h_yahoo,l_yahoo,p_yahoo,v_yahoo=parseToList_yahoo(symbol,year)

	if len(d_google)==0:
		return 	d_yahoo,h_yahoo,l_yahoo,p_yahoo,v_yahoo	

	d=[]
	h=[]
	l=[]
	p=[]
	v=[]
	i=0
	j=0
	GOOG_DONE=False
	YHOO_DONE=False
	while (not GOOG_DONE) and (not YHOO_DONE):
		
		if i>len(d_google)-1 : 
			GOOG_DONE=True
			i=len(d_google)-1
		if j>len(d_yahoo) -1:
			YHOO_DONE=True
			j=len(d_yahoo)-1
		
		if GOOG_DONE or YHOO_DONE:
			break

		d_goog=toDaniDate(d_google[i])
		d_yhoo=toDaniDate(d_yahoo[j])
		
		if d_goog==d_yhoo:
			d.append(d_google[i])
			h.append(h_google[i])
			l.append(l_google[i])
			p.append(p_google[i])
			v.append(v_google[i])
			
			if DEBUG:
				print "added     Google   Yahoo"
				print "Google equal yahoo"
				print d[-1],d_google[i],d_yahoo[j]
				print h[-1],h_google[i],h_yahoo[j]
				print l[-1],l_google[i],l_yahoo[j]
				print p[-1],p_google[i],p_yahoo[j]
				print v[-1],v_google[i],v_yahoo[j]
				print i,j
			i+=1
			j+=1
			#print i,j
		elif laterThan(d_google,d_yahoo):
			d.append(d_yahoo[j])
			h.append(h_yahoo[j])
			l.append(l_yahoo[j])
			p.append(p_yahoo[j])
			v.append(v_yahoo[j])
			
			if DEBUG:
				print "added    Google   Yahoo"
				print "google later than yahoo"
				print d[-1],d_google[i],d_yahoo[j]
				print h[-1],h_google[i],h_yahoo[j]
				print l[-1],l_google[i],l_yahoo[j]
				print p[-1],p_google[i],p_yahoo[j]
				print v[-1],v_google[i],v_yahoo[j]
				print i,j
			j+=1
			#print i,j
		else:
			d.append(d_google[i])
			h.append(h_google[i])
			l.append(l_google[i])
			p.append(p_google[i])
			v.append(v_google[i])
			
			if DEBUG:
				print "added     Google   Yahoo"
				print "else:yahoo later than google"
				print d[-1],d_google[i],d_yahoo[j]
				print h[-1],h_google[i],h_yahoo[j]
				print l[-1],l_google[i],l_yahoo[j]
				print p[-1],p_google[i],p_yahoo[j]
				print v[-1],v_google[i],v_yahoo[j]
				print i,j
			i+=1
			#print i,j
		
	p=array(p)
	h=array(h)
	l=array(l)
	v=array(v)
	
	return d,h,l,p,v,p #The last p overwrites the closes
	
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

	dates,highs,lows,prices,volume =pullIntraDay("MSFT")
	#getSplitFast("MSFT")
	
	#UIHC from 2008 is lacking a lot of stock data 
	
	""" Google Vs Yahoo Vs Mixed"""
	#a,b,c,d,e,f=parseToList_yahoo("AAPL",2005)#APPZ
	#a2,b2,c2,d2,e2,f2=parseToList_google("AAPL",2005)
	#a3,b3,c3,d3,e3,f3= parseToList("AAPL",2005)
	#for x,y,z,w,m,n in zip(a,a3,a2,c,c3,c2):
	#	print x,y,z,w,m,n
	#for x,y,z,w,p,q in zip(a,a3,c,c3,e,e3):
	#	print x,y,z,w,p,q
	#for x,y,z,e in zip(a2,b2,c2,d2):
	#	print x,y,z,e
		
	#print getSplitTime("AAPL",[0,1,2005],[4,1,2006])
	#print checkSplit("AAPL")
	#getCurrentData("RNIN")
	
