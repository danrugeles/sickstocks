from earningCalculator import *

if __name__=="__main__":
	milestones=[]
	transactions=[]
	#Bind LOAN with the one defined in earningcalculator!! the value must change as it iterates through the functions and there ust be only one LOAN


	#CREATE A CLASS Is the right way to go!


	for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:
		finalresults=[]		
		for PEAKDURATION in peakdurations:		
			print "exchange,peakincrement",exchange,PEAKDURATION
			for PEAKINCREMENT in peakincrements:
				for INSURANCEDURATION in insurancedurations:
					for INSURANCEINCREMENT in insuranceincrements:
						for SPLITFILTER in splitfilter:
							for STOPLIMIT in stoplimits:
								for EARNINGLIMIT in earninglimits:
									e=Earning()
									milestones[:]=[]
									transactions[:]=[]
									for year in range(2000,2014):#2000,2014	
										#**1. Get all transactions and milestones
										base=""+str(year)
										name=exchange+"_"+str(PEAKDURATION)+"_"+str(PEAKINCREMENT)+"_"+str(INSURANCEDURATION)+"_"+str(INSURANCEINCREMENT)+"_"+str(SPLITFILTER)+"_"+str(STOPLIMIT)+"_"+str(EARNINGLIMIT)
										base=base+"/Report_"+name+".csv"										
										transactions,milestones=getMilestones(base,transactions,milestones)
									
									#**2. Calculate Capital		
									capital=calculateEarning(e,transactions,milestones)	
									
									#**3. Append capital to finalresults
									appendResults(e,finalresults)		
																		
										
		writeFinalResults(e,finalresults)
