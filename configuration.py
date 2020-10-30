from io_device import IoDevice
from process import Process
import random

class Configuration:

	def __init__(self,generateProcessesAtRandom, timeSlice, ioDevices, processes):
		self.generateProcessesAtRandom = generateProcessesAtRandom
		self.timeSlice = timeSlice

		self.ioDevices = []

		for device in ioDevices:
			self.ioDevices.append(IoDevice(**device))

		self.processes = []

		if not self.generateProcessesAtRandom:
			for task in processes:
				self.processes.append(Process(**task))
		else:
			numberOfProcesses = random.randint(0,100)

			for _ in range(0, numberOfProcesses):
				arrivalTime = random.randint(0,100)
				self.processes.append(Process(arrivalTime))