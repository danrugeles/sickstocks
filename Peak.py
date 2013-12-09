class Peak:
	def __init__(self,start,stop,minimum,maximum,percentage):
		self.start=start
		self.stop=stop
		self.maximum=maximum
		self.minimum=minimum
		self.percentage=percentage

	def update(self,start,stop,minimum,maximum,percentage):
		self.start=start
		self.stop=stop
		self.maximum=maximum
		self.minimum=minimum
		self.percentage=percentage

	def __str__(self):
		return "start: "+str(self.start)+" - stop: "+str(self.stop)+"\npercentage: "+str(self.percentage)
