import numpy as np
import mycsv



#** Intuition
# The strategy with overall higher rankings will be the best.
def findStrategy(path,year,exchange):

	data=mycsv.getCol(path+str(year)+"_"+exchange,range(7))
	
	#data=np.array([[1,2.2],[2,2.2],[1,2.2],[2,3.2],[1,2.2],[2,3.2],[1,3.2],[2,3.2],[1,3.2],[2,2.2]])

	data=np.asarray(data[1:])
	
	bestparameters=[]

	for parameter in data.T:
		value_freq={}
		for ranking,value in enumerate(parameter):
			try:
				value_freq[str(value)]+=ranking
			except KeyError:
				value_freq[str(value)]=ranking

		print value_freq
		bestparametervalueindex=np.argmin(value_freq.values())
		bestparametervalue=value_freq.keys()[bestparametervalueindex]
		bestparameters.append(bestparametervalue)

	return bestparameters


if __name__=="__main__":

	for year in range(2013,1999,-1):#2013,1999,-1
		for exchange in ["OTCBB"]:#"NASDAQ","NYSE","OTCBB","AMEX"	
			print year,exchange
			path="FinalResults/"
			print findStrategy(path,year,exchange)
			print ""
	




