from earningCalculator import *

if __name__=="__main__":
	transactions=[]
	milestones=[]

	for year in range(2012,2013):#2000,2014
		for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:
			finalresults=[]
			for PEAKDURATION in peakdurations:		
				print "year,exchange,peakincrement",year,exchange,PEAKDURATION
				for PEAKINCREMENT in peakincrements:
					for INSURANCEDURATION in insurancedurations:
						for INSURANCEINCREMENT in insuranceincrements:
							for SPLITFILTER in splitfilter:
								for STOPLIMIT in stoplimits:
									for EARNINGLIMIT in earninglimits:
										e=Earning()
										
										#**1. Get all transactions
										milestones[:]=[]	
										#the following was never adeed, why?
										#transactions[:]=[]	
										base="../../../../Results/"+str(year)

										name=exchange+"_"+str(PEAKDURATION)+"_"+str(PEAKINCREMENT)+"_"+str(INSURANCEDURATION)+"_"+str(INSURANCEINCREMENT)+"_"+str(SPLITFILTER)+"_"+str(STOPLIMIT)+"_"+str(EARNINGLIMIT)
										base=base+"/Report_"+name+".csv"									
										transactions,milestones=getMilestones(base,transactions,milestones)
										
										#**2. Calculate Capital		
										capital=calculateEarning(e,transactions,milestones)	
									
										#**3. Append capital to finalresults
										appendResults(e,finalresults)	
										appendResults(finalresults,capital,LOAN)
																															
			writeFinalResults(finalresults)
			


