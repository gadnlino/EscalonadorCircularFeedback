from copy import deepcopy
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

    def start(self):
        self.time = 0
        self.runningTimeSliceLength = 0
        self.freePID = 2

        self.runningProcess = None
        self.cpuQueues = {
            "low": LinkedList(),
            "high": LinkedList()
        }

        self.ioData = {}

        for ioDevice in self.configuration.ioDevices:
            if ioDevice.returnPriority != "high" and ioDevice.returnPriority != "low":
                print("invalid i/o device: ", ioDevice.name)
                continue # ignora invalido
            # Tempo da IO  / Prioridade de retorno da IO / Fila de processos para usar a IO / Processo atual usando a IO / Tempo que o processo terminará de usar a IO
            self.ioData[ioDevice.name] = (ioDevice.requiredTime, ioDevice.returnPriority, LinkedList(), None, None)

        self.log("starting...")

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
                if self.runningProcess == None:
                    newProcess.ppid = 1 # kernel
                else:
                    newProcess.ppid = self.runningProcess.pid
                # Time
                newProcess.processTime = 0
                # Priority
                newProcess.priority = "high"
                # State 2
                newProcess.state = ProcessState.READY
                self.cpuQueues.get("high").add(newProcess)
                self.log("novo pid " + str(newProcess.pid))
            
            # interrupções de i/o prontas
            for ioDevice in self.ioData:
                ioTime, ioReturnPriority, ioQueue, ioWaitingProcess, ioEndTime = self.ioData.get(ioDevice)
                if ioWaitingProcess != None and self.time == ioEndTime:
                    ioWaitingProcess.processTime = ioWaitingProcess.processTime + 1
                    if ioWaitingProcess.processTime == ioWaitingProcess.totalTime:
                        ioWaitingProcess.state = ProcessState.FINISHED
                        ioWaitingProcess.completionTime = self.time
                        self.log("pid " + str(ioWaitingProcess.pid) + " terminou i/o e encerrou")
                    else:
                        ioWaitingProcess.state = ProcessState.READY
                        ioWaitingProcess.priority = ioReturnPriority
                        self.cpuQueues.get(ioReturnPriority).add(ioWaitingProcess)
                        self.log("pid " + str(ioWaitingProcess.pid) + " terminou i/o e foi para a fila " + str(ioReturnPriority))
                    ioWaitingProcess = ioEndTime = None
                    self.ioData[ioDevice] = (ioTime, ioReturnPriority, ioQueue, ioWaitingProcess, ioEndTime)

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
                self.runningProcess.priority = "low"
                self.cpuQueues.get("low").add(self.runningProcess)
                self.log("pid " + str(self.runningProcess.pid) + " usou todo o time slice")
                self.runningProcess = None
                self.runningTimeSliceLength = 0
            # testa se há interrupções de i/o pro processo executando
            if self.runningProcess != None:
                self.checkRunningProcessInterruptions()
            while self.runningProcess == None and any(self.cpuQueues[queue].peek() != None for queue in self.cpuQueues):
                if self.cpuQueues["high"].peek() != None:
                    self.runningProcess = self.cpuQueues["high"].pop()
                    self.log("pid " + str(self.runningProcess.pid) + " vindo da fila de alta prioridade")
                elif self.cpuQueues["low"].peek() != None:
                    self.runningProcess = self.cpuQueues["low"].pop()
                    self.log("pid " + str(self.runningProcess.pid) + " vindo da fila de baixa prioridade")
                self.runningProcess.state = ProcessState.EXECUTION
                self.runningTimeSliceLength = 0
                
                # testa se há interrupções de i/o pro processo ao adicionar
                self.checkRunningProcessInterruptions()
            
            # início das operações de i/o
            for ioDevice in self.ioData:
                ioTime, ioReturnPriority, ioQueue, ioWaitingProcess, ioEndTime = self.ioData.get(ioDevice)
                if ioWaitingProcess == None and ioQueue.peek() != None:
                    ioWaitingProcess = ioQueue.pop()
                    self.log("pid " + str(ioWaitingProcess.pid) + " iniciou i/o " + ioDevice)
                    ioEndTime = self.time + ioTime
                self.ioData[ioDevice] = (ioTime, ioReturnPriority, ioQueue, ioWaitingProcess, ioEndTime)
            
            if self.runningProcess != None:
                self.runningProcess.processTime = self.runningProcess.processTime + 1
                self.runningTimeSliceLength = self.runningTimeSliceLength + 1
            self.time = self.time + 1

            if(self.runningProcess != None):
                self.log("pid " + str(self.runningProcess.pid) + " executando, " + str(self.runningProcess.processTime) + "/" + str(self.runningProcess.totalTime))
                if (self.runningProcess.processTime > self.runningProcess.totalTime): 
                    sys.exit(1)
            else:
                self.log ("ocioso")

    def log(self, value):
        print(self.time, ": ", value)

    def checkRunningProcessInterruptions(self): 
        for interruption in filter(lambda i: i.processTime == self.runningProcess.processTime, self.runningProcess.interruptions):
            self.log("pid " + str(self.runningProcess.pid) + " pediu i/o " + interruption.category)
            ioQueue = self.ioData.get(interruption.category)[2]
            ioQueue.add(self.runningProcess)
            self.runningProcess.state = ProcessState.BLOCKED
            self.runningProcess = None
            self.runningTimeSliceLength = 0
            break

    # checa as filas e os processos que ainda vao entrar pra ver se posso parar de executar
    # retorna True se ainda houver processos para executar; falso se não houver
    def hasProcesses(self):
        return self.runningProcess != None or \
            any(self.ioData[queue][2].peek() != None or self.ioData[queue][3] != None for queue in self.ioData) or \
            any(self.cpuQueues[queue].peek() != None for queue in self.cpuQueues) or \
            any(process.arrivalTime >= self.time for process in self.configuration.processes)


    



