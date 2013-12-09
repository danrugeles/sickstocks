import csv
from Date import *
from numpy import *
from Transaction import *
#import itertools
#from Plot import *

transactions=[]
investments=[]
milestones=[]
# Value of each individual investment
INVESTMENT=1000.0
#Amount Invested
LOAN=0.0
capital=0.0
capital_history=[]
time_transaction=[]




peakdurations=[10,15,18,22]#18
peakincrements=[1.2,1.6,2,2.5]#1.8
insurancedurations=[8,10,15,19]#15
insuranceincrements=[-0.1,-0.15,-0.2,-0.25]#-0.2
stoplimits=[1.1,1.15,1.2,1.25,1.3]#1.2
earninglimits=[0.4,0.5,0.6,0.7,0.8]#0.75
splitfilter=[True,False]


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

	base="2013/Report_OTCBB_10_1.2_8_-0.1_False_1.15_0.4.csv"

	#**1. Get all transactions
	with open(base,"rb") as csvfile:
		report=csv.reader(csvfile,delimiter=',')
		for idx,row in enumerate(report):
			if idx>0:
				transactions.append(Transaction(row[0],toDaniDate(row[1]),float(row[2]),toDaniDate(row[3]),float(row[4]),float(row[-1])))                     
				milestones.append((toDaniDate(row[1]),len(transactions)-1))
				milestones.append((toDaniDate(row[3]),len(transactions)-1))
	
	for t in  transactions:
		print t


	#**2. Sort all milestones inplace
	for idx,t in enumerate(milestones):
		for idx2 in range(idx+1,len(milestones)):
			if laterThan(milestones[idx][0],milestones[idx2][0]):
				swap(milestones,idx,idx2)


	for m in milestones:
		print m
	#**Simulate
	for t in milestones:
		#print "MILESTONE",transactions[t[1]].BOUGHT
		if not transactions[t[1]].BOUGHT:
			if transactions[t[1]].buyprice!=0:
				transactions[t[1]].BOUGHT=True
				if capital<INVESTMENT:
					LOAN+=INVESTMENT
					capital+=INVESTMENT
				capital-=INVESTMENT
				time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
				print "Short",transactions[t[1]].symbol,transactions[t[1]].shortdate,transactions[t[1]].shortprice,capital,LOAN
		else:
			transactions[t[1]].SOLD=True
			capital+=INVESTMENT*(transactions[t[1]].profit+1)
			time_transaction.append(Transaction.toReadableDateNoYear(transactions[t[1]].buydate))
			print "Rebuy",transactions[t[1]].symbol,transactions[t[1]].buydate,transactions[t[1]].buyprice,transactions[t[1]].profit,capital,LOAN
		#print "capital,Loan", capital,LOAN, "\n"	
		capital_history.append(capital)

	print capital_history
	print time_transaction[3:5]
	

	#plotEarningPerYear(capital_history,time_transaction,2012)







