import csv
from Date import *
from numpy import *
from Transaction import *
#import itertools
from Plot import *
import operator

transactions=[]


# Value of each individual investment
INVESTMENT=1000

#Amount Invested
LOAN=0
capital=0

peakdurations=[10,15,18,22]#18
peakincrements=[1.2,1.6,2,2.5]#1.8
insurancedurations=[8,10,15,19]#15
insuranceincrements=[-0.1,-0.15,-0.2,-0.25]#-0.2
stoplimits=[1.1,1.15,1.2,1.25,1.3]#1.2
earninglimits=[0.4,0.5,0.6,0.7,0.8]#0.75
splitfilter=[True,False]

SAVEHISTORY=False

if SAVEHISTORY:
	capital_history=[]
	time_transaction=[]

def swap(array,one,two):
	temp=array[one]
	array[one]=array[two]
	array[two]=temp

class Investment:
	
	#id_generator=itertools.count(0)

	def __init__(self,transaction):
		self.profit=transaction.profit
		#self.id=next(self.id_generator)

	def reinvest(self,transaction):
		self.profit=transaction.profit*self.profit
	
	def __str__(self):
		return str(self.profit)

if __name__=="__main__":
	for year in range(2011,2014):#2000,2014
		finalresults=[]
		for PEAKDURATION in peakdurations:	
			print year,PEAKDURATION	
			for PEAKINCREMENT in peakincrements:
				for INSURANCEDURATION in insurancedurations:
					for INSURANCEINCREMENT in insuranceincrements:
						for SPLITFILTER in splitfilter:
							for STOPLIMIT in stoplimits:
								for EARNINGLIMIT in earninglimits:
									capital=0
									LOAN=0

									#**1. Get all transactions
									milestones=[]		
									base=""+str(year)
									for exchange in ["NASDAQ","NYSE","OTCBB"]:
										name=exchange+"_"+str(PEAKDURATION)+"_"+str(PEAKINCREMENT)+"_"+str(INSURANCEDURATION)+"_"+str(INSURANCEINCREMENT)+"_"+str(SPLITFILTER)+"_"+str(STOPLIMIT)+"_"+str(EARNINGLIMIT)
										#name=exchange
										base=base+"/Report_"+name+".csv"
										#print base
										with open(base,"rb") as csvfile:
											report=csv.reader(csvfile,delimiter=',')
											for idx,row in enumerate(report):
												if idx>0:
													transactions.append(Transaction(row[0],toDaniDate(row[1]),float(row[2]),toDaniDate(row[3]),float(row[4]),float(row[-1])))                     
													milestones.append((toDaniDate(row[1]),len(transactions)-1))
													milestones.append((toDaniDate(row[3]),len(transactions)-1))  		
										base=""+str(year)


									#**2. Sort all milestones inplace
									for idx,t in enumerate(milestones):
										for idx2 in range(idx+1,len(milestones)):
											if laterThan(milestones[idx][0],milestones[idx2][0]):
												swap(milestones,idx,idx2)
		
									#**3. Simulate
									for t in milestones:
										if not transactions[t[1]].BOUGHT:
											transactions[t[1]].BOUGHT=True
											if capital<INVESTMENT:
												LOAN+=INVESTMENT
												capital+=INVESTMENT
											capital-=INVESTMENT
									
											if SAVEHISTORY:
												time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
											#print "transacion",transactions[t[1]]
										else:
											transactions[t[1]].SOLD=True
											#print "transacion",transactions[t[1]]
											capital+=INVESTMENT*(transactions[t[1]].profit+1)

											if SAVEHISTORY:
												time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
												
										if SAVEHISTORY:
											capital_history.append(capital)

									finalresults.append([str(PEAKDURATION),str(PEAKINCREMENT),str(INSURANCEDURATION),str(INSURANCEINCREMENT),str(SPLITFILTER),str(STOPLIMIT),str(EARNINGLIMIT),str(LOAN),str(capital),capital/LOAN*100.0])

		#Order final results capital
		finalresults=sorted(finalresults,key=operator.itemgetter(-1),reverse=True)
		
		#Save final results per year
		with open("FinalResults/"+str(year),"w") as w:			
			w.write("PEAKDURATION,PEAKINCREMENT,INSURANCEDURATION,INSURANCEINCREMENT,SPLITFILTER,STOPLIMIT,EARNNGLIMIT,LOAN,CAPITAL,YIELD\n")
			for f in finalresults:
				w.write(",".join(f[:-1])+","+str(f[-1])+"\n")

	if SAVEHISTORY:
		print capital_history
		print time_transaction
		#plotEarningPerYear(capital_history,time_transaction,2012)







