from earningCalculator import *

if __name__=="__main__":

	transactions=[]
	milestones=[]

	base="2013/Report_OTCBB_10_1.2_8_-0.1_False_1.15_0.4.csv"

	#**1. Get all transactions
	transactions,milestones=getMilestones(base,transactions,milestones)
	
	#**2. Calculate Capital		
	capital=calculateEarning(transactions,milestones)

	print capital
