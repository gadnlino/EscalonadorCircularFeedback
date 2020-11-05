from models.io_device import IoDevice
from models.process import Process
from models.interruption import Interruption
import random

class Configuration:

	def __init__(self, timeSlice, ioDevices, processes, generateProcessesAtRandom = False):
		self.generateProcessesAtRandom = generateProcessesAtRandom
		self.timeSlice = timeSlice

		self.ioDevices = []

		for device in ioDevices:
			self.ioDevices.append(IoDevice(**device))

		self.processes = []

		#Se a flag 'generateProcessesAtRandom' for false, devo pegar os processos
		#definidos na propriedade 'processes' da configuração
		if not self.generateProcessesAtRandom:
			for task in processes:
				self.processes.append(Process(**task))
		#caso contrário, ignorar a propriedade e gerar aleatoriamente
		#os processos
		else:
			numberOfProcesses = random.randint(1,25)

			for _ in range(numberOfProcesses):
				arrivalTime = random.randint(0,50)
				totalTime = random.randint(1,50)

				interruptions = []

				if (totalTime > 1):
					interruption_times = random.sample(range(totalTime-1), min(totalTime-1, random.randint(0, 4)))

					for time in interruption_times:
						category = random.choice(["hardDisk", "magneticTape", "printer"])
						interruptions.append(Interruption(category, time))

				self.processes.append(Process(arrivalTime, totalTime, interruptions=interruptions))