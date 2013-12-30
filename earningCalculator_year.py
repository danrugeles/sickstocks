from earningCalculator import *

if __name__=="__main__":
	transactions=[]
	milestones=[]
	
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
									e=Earning()

									#**1. Get all transactions
									milestones=[]		
									base=""+str(year)
									for exchange in ["NASDAQ","NYSE","OTCBB","AMEX"]:
										name=exchange+"_"+str(PEAKDURATION)+"_"+str(PEAKINCREMENT)+"_"+str(INSURANCEDURATION)+"_"+str(INSURANCEINCREMENT)+"_"+str(SPLITFILTER)+"_"+str(STOPLIMIT)+"_"+str(EARNINGLIMIT)
										base=base+"/Report_"+name+".csv"													
										transactions,milestones=getMilestones(base,transactions,milestones)
										base=""+str(year)
										
									#**2. Calculate Capital		
									capital=calculateEarning(e,transactions,milestones)	
								
									#**3. Append capital to finalresults
									appendResults(e,finalresults)	
																		
		writeFinalResults(finalresults)


