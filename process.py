class Process:

	def __init__(self, arrivalTime):
		self.arrivalTime = arrivalTime
		self.pid = None
		self.ppid = None
		self.status = None
		self.priority = None
		self.order = None
		self.completionTime = float('inf')