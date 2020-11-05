from models.interruption import Interruption
from enum import Enum

class Process:

	def __init__(self, arrivalTime, totalTime, interruptions = []):
		self.arrivalTime = arrivalTime
		self.totalTime = totalTime
		self.processTime = None
		self.pid = None
		self.ppid = None
		self.state = ProcessState.NONEXISTENT
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
	NONEXISTENT = 1
	NEW = 2
	READY = 3
	EXECUTION = 4
	BLOCKED = 5
	FINISHED = 6