import csv
from Date import *
from numpy import *
from Transaction import *
from Plot import *
import operator

# Value of each individual INVESTMENT
INVESTMENT=1000

#Amount Invested
e.LOAN=0.0
e.capital=0.0


class Earning:
	
	INVESTMENT=1000
	
	def __init__(self):
		self.LOAN=0.0
		self.capital=0.0


SAVEHISTORY=False

if SAVEHISTORY:
	capital_history=[]
	time_transaction=[]
	

"""peakdurations=[10,15,18,22]#18
peakincrements=[1.2,1.6,2,2.5]#1.8
insurancedurations=[8,10,15,19]#15
insuranceincrements=[-0.1,-0.15,-0.2,-0.25]#-0.2
stoplimits=[1.1,1.15,1.2,1.25,1.3]#1.2
earninglimits=[0.4,0.5,0.6,0.7,0.8]#0.75
splitfilter=[True,False]"""

peakdurations=[10,15,18,22]#18
peakincrements=[1.2,1.6,1.8,2.2]#1.8
insurancedurations=[8,10,15,19]#15
insuranceincrements=[-0.05,-0.12,-0.17,-0.25]#-0.2
stoplimits=[1.1,1.15,1.2,1.25,1.3]#1.2
earninglimits=[0.45,0.55,0.65,0.75,0.85]#0.75
splitfilter=[True,False]
	

def swap(array,one,two):
	temp=array[one]
	array[one]=array[two]
	array[two]=temp


def getMilestones(base,transactions,milestones):
	with open(base,"rb") as csvfile:
		report=csv.reader(csvfile,delimiter=',')
		for idx,row in enumerate(report):
			if idx>0:
				transactions.append(Transaction(row[0],toDaniDate(row[1]),float(row[2]),toDaniDate(row[3]),float(row[4]),float(row[-1])))                     
				milestones.append((toDaniDate(row[1]),len(transactions)-1))
				milestones.append((toDaniDate(row[3]),len(transactions)-1))  
	return transactions,milestones
	
	

def calculateEarning(e,transactions,milestones):

	#**A. Sort all milestones inplace
	for idx,t in enumerate(milestones):
		for idx2 in range(idx+1,len(milestones)):
			if laterThan(milestones[idx][0],milestones[idx2][0]):
				swap(milestones,idx,idx2)

	#**B. Simulate
	for t in milestones:
		if not transactions[t[1]].BOUGHT:
			transactions[t[1]].BOUGHT=True
			if e.capital<e.INVESTMENT:
				e.LOAN+=e.INVESTMENT
				e.capital+=e.INVESTMENT
			e.capital-=e.INVESTMENT
	
			if SAVEHISTORY:
				time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
			#print "Short",transactions[t[1]].symbol,transactions[t[1]].shortdate,transactions[t[1]].shortprice,e.capital,e.LOAN
		else:
			transactions[t[1]].SOLD=True
			e.capital+=e.INVESTMENT*(transactions[t[1]].profit+1)
			#print "Rebuy",transactions[t[1]].symbol,transactions[t[1]].buydate,transactions[t[1]].buyprice,transactions[t[1]].profit,e.capital,e.LOAN
			if SAVEHISTORY:
				time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
				
		if SAVEHISTORY:
			capital_history.append(e.capital)
			
	if SAVEHISTORY:
		print capital_history
		print time_transaction
		plotEarningPerYear(capital_history,time_transaction,2012)

	return e.capital
	
	
def writeFinalResults(e,finalresults):
	#Order final results e.capital
	finalresults=sorted(finalresults,key=operator.itemgetter(-1),reverse=True)
	
	#Save final results per year
	with open("FinalResults/"+str(year),"w") as w:			
		w.write("PEAKDURATION,PEAKINCREMENT,INSURANCEDURATION,INSURANCEINCREMENT,SPLITFILTER,STOPLIMIT,EARNNGLIMIT,e.LOAN,e.capital,YIELD\n")
		for f in finalresults:
			w.write(",".join(f[:-1])+","+str(f[-1])+"\n")

def appendResults(e,finalresults):
	try:
		finalresults.append([str(PEAKDURATION),str(PEAKINCREMENT),str(INSURANCEDURATION),str(INSURANCEINCREMENT),str(SPLITFILTER),str(STOPLIMIT),str(EARNINGLIMIT),str(e.LOAN),str(e.capital),e.capital/e.LOAN*100.0])
	except ZeroDivisionError:
		if len(milestones)!=0:								
			assert(False)
		else:
			finalresults.append([str(PEAKDURATION),str(PEAKINCREMENT),str(INSURANCEDURATION),str(INSURANCEINCREMENT),str(SPLITFILTER),str(STOPLIMIT),str(EARNINGLIMIT),str(e.LOAN),str(e.capital),"0.0"])

			
