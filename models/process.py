from models.interruption import Interruption
from enum import Enum

class Process:

	def __init__(self, arrivalTime, totalTime, interruptions = []):
		self.arrivalTime = arrivalTime
		self.pid = None
		self.ppid = None
		self.state = ProcessState.NEW
		self.priority = None
		self.order = None
		self.completionTime = float('inf')

		self.interruptions = []

		for a in interruptions:
			if isinstance(a, dict):
				self.interruptions.append(Interruption(**a))
			elif isinstance(a, Interruption):
				self.interruptions.append(a)

class ProcessState(Enum):
	NEW = 1
	READY = 2
	EXECUTION = 3
	BLOCKED = 4
	FINISHED = 5