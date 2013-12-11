import re
#from sickstocksimulator import dates
## month,day,year

def getDate(dates,time):
	try:
		match=re.search(r"([\w]*)-([\w]*)-([\w]*)",dates[time])
		return [int(match.group(2))-1,int(match.group(3)),int(match.group(1))]
	except IndexError:
		match=re.search(r"([\w]*)-([\w]*)-([\w]*)",dates[-1])
		#print "Warning: getDate(time) returned a future date after:",[int(match.group(2)),int(match.group(3)),int(match.group(1))]
		return [int(match.group(2))-1,int(match.group(3)),int(match.group(1))]

#DaniDate Format: [month-1,day,year]

def yyyymmddToDaniDate(date):
	year=date[:5]
	month=date[5:7]
	day=date[7:]	
	return [int(month)-1,int(day),int(year)]


def toDaniDate(date):
	match=re.search(r"([\w]*)-([\w]*)-([\w]*)",date)
	return [int(match.group(2))-1,int(match.group(3)),int(match.group(1))]

#From Yahoo finance

def getMonthDiff(start,stop):
	#**Days Difference
	daydiff=stop[1]-start[1]

	if daydiff<0:
		stop[0]=(stop[0]-1)%12

	#**Month Difference
	if stop[0]>=start[0]:
		monthdiff=stop[0]-start[0]
	else:
		stop[2]=stop[2]-1
		monthdiff=(stop[0]+11)-start[0]+2

	#**Year Difference
	if stop[2]>=start[2]:
		return monthdiff
	else:
		print "Warning: negative time difference, returning 0"
		return 0

def getNextStop(start):
	stop=[start[0],start[1],start[2]]
	if start[0]+3>=12:
		stop[2]=start[2]+1
	stop[0]=(start[0]+12+3)%12
	return stop

def laterThan(first,second):
	if first[2]>second[2]:
		return True
	if first[2]==second[2]:
		if first[0]>second[0]:
			return True
		if first[0]==second[0]:
			if first[1]>second[1]:
				return True
	return False
