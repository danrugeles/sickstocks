#from sickstocksimulator import INSURANCEINCREMENT,STOPLIMIT,EARNINGLIMIT<
import numpy as np
import itertools


# Money expected to trade per transaction
INVESTMENT=50000.0

class Transaction:
	#transactions=[]
	dates=[]
	id_generator=itertools.count(0)
	INSURANCEINCREMENT=0
	stoplimits=[]
	earninglimits=[]
	transaction_container=[]
	
	def __init__(self,symbol=None,shortdate=None,shortprice=None,buydate=None,buyprice=None,profit=None,BOUGHT=None,SOLD=None):
		#self.transactions[:]=[]
		self.dates[:]=[]
		self.symbol=symbol
		self.shortdate=shortdate
		self.shortprice=shortprice
		self.buydate=buydate
		self.buyprice=buyprice
		self.profit=profit
		self.BOUGHT=False
		self.SOLD=False
		self.id=next(self.id_generator)
		self.transaction_container[:]=[]
		
	def getDate(self,time):
		try:
			return self.dates[time]
		except IndexError:
			return self.dates[-1]+"(future)"

	def constructTransactionContainer(self):
		if len(self.earninglimits)==0 or len(self.stoplimits)==0:
			print "Warning: earninglimits y/o stoplimits has not been initialized" 
		filler = np.frompyfunc(lambda x: list(), 1, 1)
		a = np.empty((np.size(self.stoplimits),np.size(self.earninglimits)), dtype=np.object)
		self.transaction_container=filler(a, a)

	#year is not currently being mnitored
	def executeTransaction(self,symbol,highs,lows,prices,volume,starttime,year):

		print prices
		#print self.dates[starttime]#Peak date
	
		
		
		#print len(self.dates)
		#print len(highs)
		prices_aux=prices[starttime:starttime+22]
		highs_aux=highs[starttime:starttime+22]
		lows_aux=lows[starttime:starttime+22]
		#print self.getDate(0),symbol
		#for d,a,b,c,v in zip(self.dates,highs,lows,prices,volume):
			#print d,a,b,c,v
		#print "\nwindow"
		for d,a,b,c in zip(self.dates[starttime:starttime+22],highs_aux,lows_aux,prices_aux):
			print d,a,b,c
		#print starttime,prices_aux
		
		
		transaction=np.array([None,None,None,None,None,None])
		BOUGHT=False
		SOLD=np.zeros((np.size(self.stoplimits),np.size(self.earninglimits)))
		
		for t in range(len(prices_aux)):
			if not BOUGHT:
				if lows_aux[t]<=prices_aux[0]*(1+self.INSURANCEINCREMENT) and volume[t]>=INVESTMENT/prices_aux[t]:
					BOUGHT=True					
					transaction[0]=symbol
					transaction[1]=self.getDate(t+starttime)
					transaction[2]=prices_aux[0]*(1+self.INSURANCEINCREMENT)
					bought_at=t
					#Post-filter
					if transaction[2]<0.9:
						return
						
						
			else:
				#printd("sellprice: "+str(transaction[1]*self.EARNINGLIMIT))
				for s_idx,STOPLIMIT in enumerate(self.stoplimits):
					for e_idx,EARNINGLIMIT in enumerate(self.earninglimits):			
						#print s_idx,e_idx,"!!!!!!!!!!!!!"					
						if  ((highs_aux[t] >= transaction[2]*STOPLIMIT or lows_aux[t] <= transaction[2]*EARNINGLIMIT)) and SOLD[s_idx][e_idx]==False and volume[t]>=50000.0/prices_aux[t]:
						
							print "Volume",volume[t],50000.0/prices_aux[t]
							transaction[3]=self.getDate(t+starttime)
							if highs_aux[t] >= transaction[2]*STOPLIMIT:
								transaction[4]=transaction[2]*STOPLIMIT
							else:
								transaction[4]=transaction[2]*EARNINGLIMIT
							transaction[5]=t-bought_at
							SOLD[s_idx][e_idx]=True
							self.transaction_container[s_idx][e_idx].append(transaction.copy())
							#print "lose or win",self.transaction_container
							return 
							
						
		#Give up and sell as tie. Assume volume is good enough
		for s_idx,STOPLIMIT in enumerate(self.stoplimits):
			for e_idx,EARNINGLIMIT in enumerate(self.earninglimits):
				#print s_idx,e_idx,"!!!!!!!!!!!!!"
				if not SOLD[s_idx][e_idx] and BOUGHT: 
					transaction[3]=self.getDate(starttime+len(prices_aux))
					transaction[4]=prices_aux[-1]
					transaction[5]=len(prices_aux)-bought_at
					self.transaction_container[s_idx][e_idx].append(transaction.copy())
					SOLD[s_idx][e_idx]=True
					#print "tie",self.transaction_container
															

	@staticmethod
	def	toReadableDateNoYear(date):
		return str(date[0]+1)+"/"+str(date[1])

	#Deprecated because of earningsReport.py
	def saveTransactions(self,exchange,year):
		np.save("Transactions/"+exchange+"_"+str(year),self.transactions)

	def createReport(self,exchange,year):
		for STOPLIMIT in range(np.size(self.stoplimits)):
			for EARNINGLIMIT in range(np.size(self.earninglimits)):
				numBought=0
				numSold=0
				wins=0
				losses=0
				totalEarnings=0.0
				base="../../../../Results/"
				#for debuggin:
				base=""
				
				with open(base+str(year)+"/Report_"+exchange+"_"+str(self.stoplimits[STOPLIMIT])+"_"+str(self.earninglimits[EARNINGLIMIT])+".csv","w") as w:
					w.write("Symbol,Shorted_on,Sold_at,Bought_on,Bought_at,Duration,Earning\n")
					for t in self.transaction_container[STOPLIMIT][EARNINGLIMIT]:
						if t[2]!=None:
							numBought+=1
						if t[3]!=None:
							numSold+=1
							if t[2]>t[4]:
								wins+=1	
							else:
								losses+=1
							if t[4]<=0.01:
								earning=0
							else:
								earning=(t[2]-t[4])/t[4]
							
							totalEarnings=totalEarnings+earning
							w.write(",".join(t.astype('|S10'))+","+str(earning)+"\n")
							#print ",".join(t.astype('|S10'))+","+str((t[2]-t[4])/t[4])

				with open(base+str(year)+"/Summary_"+exchange+"_"+str(self.stoplimits[STOPLIMIT])+"_"+str(self.earninglimits[EARNINGLIMIT])+".txt","w") as w2:
					w2.write("numBought="+str(numBought)+"\nnumSold="+str(numSold)+"\nwins="+str(wins)+"\nlosses="+str(losses)+"\ntotalEarnings="+str(totalEarnings))
					
	



