from earningCalculator import *

if __name__=="__main__":

	name="OTCBB_10_1.2_8_-0.1_True_1.15_0.4"

	milestones=[]
	transactions=[]
	
	for year in range(2000,2014):#2000,2014	
		#**1. Get all transactions and milestones
		base=""+str(year)
		base=base+"/Report_"+name+".csv"		
		transactions,milestones=getMilestones(base,transactions,milestones)
						
	#**2. Calculate Capital		
	capital=calculateEarning(transactions,milestones)	
	
	print capital	

