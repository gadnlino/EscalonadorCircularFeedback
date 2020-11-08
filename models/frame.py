import json

class Frame:
    def __init__(self):
        self.data = {
            'pid': None,
            'processor': {
                'low': [],
                'medium': [],
                'high': []
            },
            'ioDevices': {
                'magneticTape': {
                    'current': None,
                    'queue': []
                },
                'printer': {
                    'current': None,
                    'queue': []
                },
                'hardDisk': {
                    'current': None,
                    'queue': []
                }
            }
        }

    def set_pid(self, pid):
        self.data['pid'] = pid

    def set_processor_queues(self, lowQueue, highQueue):
        self.data['processor']['low'] = lowQueue
        self.data['processor']['high'] = highQueue

    def set_io_devices_queue(self, magneticTapeQueue, printerQueue, hardDiskQueue):
        self.data['ioDevices']['magneticTape']['queue'] = magneticTapeQueue
        self.data['ioDevices']['printer']['queue'] = printerQueue
        self.data['ioDevices']['hardDisk']['queue'] = hardDiskQueue
    
    def set_current_io_processes(self, currentMagneticTape, currentPrinter, currentHardDisk):
        self.data['ioDevices']['magneticTape']['current'] = currentMagneticTape
        self.data['ioDevices']['printer']['current'] = currentPrinter
        self.data['ioDevices']['hardDisk']['current'] = currentHardDisk