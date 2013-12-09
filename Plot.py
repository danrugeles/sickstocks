import matplotlib.pyplot as plt

def plotEarningPerYear(a,b,year):
	plt.plot(a, 'r-')
	plt.xticks(range(len(b)), b, rotation="vertical",size='small')
	plt.title("Investment "+str(year))
	plt.ylabel("Capital")

	plt.grid(True)
	plt.show()


if __name__=="__main__":

	a=[10,11,12,13,14,15]
	b=['10ASD','11','12','13','14','15']
	plotEarningPerYear(a,b,2012)

