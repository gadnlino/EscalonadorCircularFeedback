from copy import deepcopy
import sys
from models.linkedList import LinkedList, Node
from models.process import Process, ProcessState
from models.frame import Frame


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
        self.frames = []

    def start(self):
        self.time = 0
        self.runningTimeSliceLength = 0
        self.freePID = 2

        self.runningProcess = None
        self.cpuQueues = self.createArray(2)
        self.cpuQueues[0] = LinkedList()  # fila de alta prioridade, "high"
        self.cpuQueues[1] = LinkedList()  # fila de baixa prioridade, "low"

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
                        interruption.done = False
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
                newProcess.ppid = 1  # kernel
                # Time
                newProcess.processTime = 0
                # Priority
                newProcess.priority = 0
                # IO
                newProcess.waitingIO = None
                # State 2
                newProcess.state = ProcessState.READY
                self.cpuQueues[0].add(newProcess)
                self.log("novo pid " + str(newProcess.pid))

            # interrupções de i/o prontas
            for i in range(self.ioDevicesCount):
                if self.ioWaitingProcesses[i] != None and self.time == self.ioEndTimes[i]:
                    self.ioWaitingProcesses[i].processTime = self.ioWaitingProcesses[i].processTime
                    self.ioWaitingProcesses[i].state = ProcessState.READY
                    self.ioWaitingProcesses[i].priority = self.ioReturnPriorities[i]
                    self.ioWaitingProcesses[i].waitingIO.done = True
                    self.ioWaitingProcesses[i].waitingIO = None
                    if (self.ioReturnPriorities[i] == "high"):
                        self.cpuQueues[0].add(self.ioWaitingProcesses[i])
                    else:
                        self.cpuQueues[1].add(self.ioWaitingProcesses[i])
                    self.log("pid " + str(self.ioWaitingProcesses[i].pid) + " terminou i/o e foi para a fila " + str(
                        self.ioReturnPriorities[i]))
                    self.ioWaitingProcesses[i] = self.ioEndTimes[i] = None

            # testa se há interrupções de i/o pro processo executando
            if self.runningProcess != None:
                self.checkRunningProcessInterruptions()

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
                self.log("pid " + str(self.runningProcess.pid) +
                         " usou todo o time slice")
                self.runningProcess = None
                self.runningTimeSliceLength = 0

            while self.runningProcess == None and any(self.cpuQueues[i].peek() != None for i in range(2)):
                if self.cpuQueues[0].peek() != None:
                    self.runningProcess = self.cpuQueues[0].pop()
                    self.log("pid " + str(self.runningProcess.pid) +
                             " vindo da fila de alta prioridade")
                elif self.cpuQueues[1].peek() != None:
                    self.runningProcess = self.cpuQueues[1].pop()
                    self.log("pid " + str(self.runningProcess.pid) +
                             " vindo da fila de baixa prioridade")
                self.runningProcess.state = ProcessState.EXECUTION
                self.runningTimeSliceLength = 0

                # testa se há interrupções de i/o pro processo ao adicionar
                self.checkRunningProcessInterruptions()

            # início das operações de i/o
            for i in range(self.ioDevicesCount):
                if self.ioWaitingProcesses[i] == None and self.ioQueues[i].peek() != None:
                    self.ioWaitingProcesses[i] = self.ioQueues[i].pop()
                    self.log(
                        "pid " + str(self.ioWaitingProcesses[i].pid) + " iniciou i/o " + self.ioDeviceNames[i])
                    self.ioEndTimes[i] = self.time + self.ioTimes[i]

            if self.runningProcess != None:
                self.runningProcess.processTime = self.runningProcess.processTime + 1
                self.runningTimeSliceLength = self.runningTimeSliceLength + 1
            self.time = self.time + 1

            if(self.runningProcess != None):
                self.log("pid " + str(self.runningProcess.pid) + " executou, " + str(
                    self.runningProcess.processTime) + "/" + str(self.runningProcess.totalTime))
            else:
                self.log("ocioso")

            self.addFrame()

        return self.frames

    def log(self, value):
        print(self.time, ": ", value)

    def checkRunningProcessInterruptions(self):
        for interruption in filter(lambda i: i.processTime == self.runningProcess.processTime and i.done == False, self.runningProcess.interruptions):
            if interruption.ioID == None or self.runningProcess.processTime + 1 == self.runningProcess.totalTime:
                self.log("pid " + str(self.runningProcess.pid) +
                         " executando interrupção inválida: " + interruption.category)
                self.log("instante: " + str(self.runningProcess.processTime +
                                            1) + " / " + str(self.runningProcess.totalTime))
                sys.exit(1)  # ignora interrupcoes a I/O invalidas.
            self.log("pid " + str(self.runningProcess.pid) +
                     " pediu i/o " + interruption.category)
            self.ioQueues[interruption.ioID].add(self.runningProcess)
            self.runningProcess.waitingIO = interruption
            self.runningProcess.state = ProcessState.BLOCKED
            self.runningProcess = None
            self.runningTimeSliceLength = 0
            break  # só pega 1 interrupção

    # checa as filas e os processos que ainda vao entrar pra ver se posso parar de executar
    # retorna True se ainda houver processos para executar; falso se não houver
    def hasProcesses(self):
        return self.runningProcess != None or \
            any(self.ioQueues[i].peek() != None or self.ioWaitingProcesses[i] != None for i in range(self.ioDevicesCount)) or \
            any(self.cpuQueues[i].peek() != None for i in range(2)) or \
            any(process.arrivalTime >=
                self.time for process in self.configuration.processes)

    # função para simular criação de array com tamanho fixo, ou calloc
    def createArray(self, length):
        return [None] * length

    def addFrame(self):
        frame = Frame()

        if self.runningProcess == None:
            frame.set_pid(None)
        else:
            frame.set_pid(self.runningProcess.pid)

        low_queue = []
        high_queue = []

        for a in self.cpuQueues[1]:
            low_queue.append(a.data.pid)

        for a in self.cpuQueues[0]:
            high_queue.append(a.data.pid)

        frame.set_processor_queues(low_queue, high_queue)

        m_queue_list = []
        m_index = next((i for i in range(self.ioDevicesCount)
                        if self.ioDeviceNames[i] == "magneticTape"), None)
        if m_index != None:
            m_queue = self.ioQueues[m_index]
            m_current = self.ioWaitingProcesses[m_index]

            if m_current != None:
                m_queue_list.append(m_current.pid)

            for node in m_queue:
                m_queue_list.append(node.data.pid)

        p_queue_list = []
        p_index = next((i for i in range(self.ioDevicesCount)
                        if self.ioDeviceNames[i] == "magneticTape"), None)
        if p_index != None:
            p_queue = self.ioQueues[p_index]
            p_current = self.ioWaitingProcesses[p_index]

            if p_current != None:
                p_queue_list.append(p_current.pid)

            for node in p_queue:
                p_queue_list.append(node.data.pid)

        h_queue_list = []
        h_index = next((i for i in range(self.ioDevicesCount)
                        if self.ioDeviceNames[i] == "magneticTape"), None)
        if h_index != None:
            h_queue = self.ioQueues[h_index]
            h_current = self.ioWaitingProcesses[h_index]

            if h_current != None:
                h_queue_list.append(h_current.pid)

            for node in h_queue:
                h_queue_list.append(node.data.pid)

        frame.set_io_devices_queue(m_queue_list, p_queue_list, h_queue_list)

        self.frames.append(frame)
