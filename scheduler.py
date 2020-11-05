from copy import deepcopy
import sys
from models.linkedList import LinkedList, Node
from models.process import Process, ProcessState

class Scheduler:
    def __init__(self, configuration):
        self.configuration = deepcopy(configuration)
        self.time = None
        self.freePID = None
        self.runningProcess = None
        self.cpuQueues = None
        self.ioData = None
        self.runningTimeSliceLength = None
        self.ioDevicesCount = None

    def start(self):
        self.time = 0
        self.runningTimeSliceLength = 0
        self.freePID = 2

        self.runningProcess = None
        self.cpuQueues = self.createArray(2)
        self.cpuQueues[0] = LinkedList() # fila de alta prioridade, "high"
        self.cpuQueues[1] = LinkedList() # fila de baixa prioridade, "low"

        self.ioDevicesCount = len(self.configuration.ioDevices)

        self.ioDeviceNames = self.createArray(self.ioDevicesCount)
        self.ioTimes = self.createArray(self.ioDevicesCount)
        self.ioReturnPriorities = self.createArray(self.ioDevicesCount)
        self.ioQueues = self.createArray(self.ioDevicesCount)
        self.ioWaitingProcesses = self.createArray(self.ioDevicesCount)
        self.ioEndTimes = self.createArray(self.ioDevicesCount)

        for i, ioDevice in enumerate(self.configuration.ioDevices):
            if ioDevice.returnPriority != "high" and ioDevice.returnPriority != "low":
                print("invalid i/o device: ", ioDevice.name)
                sys.exit(1)
            ioDevice.ioID = i

            for process in self.configuration.processes:
                for interruption in process.interruptions:
                    if interruption.category == ioDevice.name:
                        interruption.ioID = ioDevice.ioID
            self.ioDeviceNames[i] = ioDevice.name
            self.ioTimes[i] = ioDevice.requiredTime
            self.ioReturnPriorities[i] = ioDevice.returnPriority
            self.ioQueues[i] = LinkedList()
            self.ioWaitingProcesses[i] = None
            self.ioEndTimes[i] = None

        self.log("iniciando...")

        # lambda object: object.time >= time
        while self.hasProcesses():
            # interrupções de processos novos
            for newProcess in filter(lambda process: process.arrivalTime == self.time, self.configuration.processes):
                # State 1
                newProcess.state = ProcessState.NEW
                # PID
                newProcess.pid = self.freePID
                self.freePID = self.freePID + 1
                # PPID
                newProcess.ppid = 1 # kernel
                # Time
                newProcess.processTime = 0
                # Priority
                newProcess.priority = 0
                # State 2
                newProcess.state = ProcessState.READY
                self.cpuQueues[0].add(newProcess)
                self.log("novo pid " + str(newProcess.pid))
            
            # interrupções de i/o prontas
            for i in range(self.ioDevicesCount):
                if self.ioWaitingProcesses[i] != None and self.time == self.ioEndTimes[i]:
                    self.ioWaitingProcesses[i].processTime = self.ioWaitingProcesses[i].processTime + 1
                    if self.ioWaitingProcesses[i].processTime == self.ioWaitingProcesses[i].totalTime: # mandar email pra professora
                        self.ioWaitingProcesses[i].state = ProcessState.FINISHED
                        self.ioWaitingProcesses[i].completionTime = self.time
                        self.log("pid " + str(self.ioWaitingProcesses[i].pid) + " terminou i/o e encerrou")
                    else:
                        self.ioWaitingProcesses[i].state = ProcessState.READY
                        self.ioWaitingProcesses[i].priority = self.ioReturnPriorities[i]
                        if (self.ioReturnPriorities[i] == "high"):
                            self.cpuQueues[0].add(self.ioWaitingProcesses[i])
                        else:
                            self.cpuQueues[1].add(self.ioWaitingProcesses[i])
                        self.log("pid " + str(self.ioWaitingProcesses[i].pid) + " terminou i/o e foi para a fila " + str(self.ioReturnPriorities[i]))
                    self.ioWaitingProcesses[i] = self.ioEndTimes[i] = None

            # teste de fim de processo
            if self.runningProcess != None and self.runningProcess.processTime == self.runningProcess.totalTime: 
                self.runningProcess.state = ProcessState.FINISHED
                self.runningProcess.completionTime = self.time
                self.log("pid " + str(self.runningProcess.pid) + " terminou")
                self.runningProcess = None
                self.runningTimeSliceLength = 0
            # teste de time slice
            if self.runningTimeSliceLength == self.configuration.timeSlice:
                self.runningProcess.state = ProcessState.READY
                self.runningProcess.priority = 1
                self.cpuQueues[1].add(self.runningProcess)
                self.log("pid " + str(self.runningProcess.pid) + " usou todo o time slice")
                self.runningProcess = None
                self.runningTimeSliceLength = 0
            # testa se há interrupções de i/o pro processo executando
            if self.runningProcess != None:
                self.checkRunningProcessInterruptions()
            while self.runningProcess == None and any(self.cpuQueues[i].peek() != None for i in range(2)):
                if self.cpuQueues[0].peek() != None:
                    self.runningProcess = self.cpuQueues[0].pop()
                    self.log("pid " + str(self.runningProcess.pid) + " vindo da fila de alta prioridade")
                elif self.cpuQueues[1].peek() != None:
                    self.runningProcess = self.cpuQueues[1].pop()
                    self.log("pid " + str(self.runningProcess.pid) + " vindo da fila de baixa prioridade")
                self.runningProcess.state = ProcessState.EXECUTION
                self.runningTimeSliceLength = 0
                
                # testa se há interrupções de i/o pro processo ao adicionar
                self.checkRunningProcessInterruptions()
            
            # início das operações de i/o
            for i in range(self.ioDevicesCount):
                if self.ioWaitingProcesses[i] == None and self.ioQueues[i].peek() != None:
                    self.ioWaitingProcesses[i] = self.ioQueues[i].pop()
                    self.log("pid " + str(self.ioWaitingProcesses[i].pid) + " iniciou i/o " + self.ioDeviceNames[i])
                    self.ioEndTimes[i] = self.time + self.ioTimes[i]
            
            if self.runningProcess != None:
                self.runningProcess.processTime = self.runningProcess.processTime + 1
                self.runningTimeSliceLength = self.runningTimeSliceLength + 1
            self.time = self.time + 1

            if(self.runningProcess != None):
                self.log("pid " + str(self.runningProcess.pid) + " executando, " + str(self.runningProcess.processTime) + "/" + str(self.runningProcess.totalTime))
            else:
                self.log ("ocioso")

    def log(self, value):
        print(self.time, ": ", value)

    def checkRunningProcessInterruptions(self): 
        for interruption in filter(lambda i: i.processTime == self.runningProcess.processTime, self.runningProcess.interruptions):
            if interruption.ioID == None:
                self.log("pid " + str(self.runningProcess.pid) + " executando interrupção inválida: " + interruption.category)
                continue # ignora interrupcoes a I/O invalidas.
            self.log("pid " + str(self.runningProcess.pid) + " pediu i/o " + interruption.category)
            self.ioQueues[interruption.ioID].add(self.runningProcess)
            self.runningProcess.state = ProcessState.BLOCKED
            self.runningProcess = None
            self.runningTimeSliceLength = 0
            break

    # checa as filas e os processos que ainda vao entrar pra ver se posso parar de executar
    # retorna True se ainda houver processos para executar; falso se não houver
    def hasProcesses(self):
        return self.runningProcess != None or \
            any(self.ioQueues[i].peek() != None or self.ioWaitingProcesses[i] != None for i in range(self.ioDevicesCount)) or \
            any(self.cpuQueues[i].peek() != None for i in range(2)) or \
            any(process.arrivalTime >= self.time for process in self.configuration.processes)

    # função para simular criação de array com tamanho fixo, ou calloc
    def createArray(self, length):
        return [None] * length

    



