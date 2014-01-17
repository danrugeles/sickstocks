#!/usr/bin/env python
import csv

__author__ = "Dan Rugeles"
__copyright__ = "Copyright 2013, Accelerometrics"
__credits__ = ["Dan Rugeles"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dan Rugeles"
__email__ = "danrugeles@gmail.com"
__status__ = "Production"

#--getCol------------------------------------------------------
"""Gets the data of a set of columns of a csv file

filename: String representing path to file
col: integer representing the column of the csv file"""
#-------------------------------------------------------------------
def getCol(filename,col):
	result=[]
	with open(filename,"rb") as csvfile:
		alldata=csv.reader(csvfile,delimiter=",")
		for idx,row in enumerate(alldata):
			if type(col)==list:
				if len(col)>1:
					result.append([row[x] for x in col])
				else:
					result.append(row[col[0]])
			elif type(col)==int:
				result.append(row[col])
			else:
				print "Warning: Incorrect type of argument in getCol() in mycsv.py"
				break
	return result


"""----------------------------*
*                              *
*   |\  /|   /\    |  |\  |    * 
*   | \/ |  /__\   |  | \ |    *
*   |    | /    \  |  |  \|    *
*                              *
*----------------------------"""
if __name__=="__main__":
	print "First\n"
	print getCol("User/73.csv",[0,1])
	print "\nSecond\n"
	print getCol("User/73.csv",0.9)
	print "\nThird\n"
	print getCol("User/73.csv",[0])
	
