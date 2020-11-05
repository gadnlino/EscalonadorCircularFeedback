import json 

class Frame:
    def __init__(self):
        self.data = {
            'pid': '',
            'processor': {
                'low': [],
                'medium': [],
                'high': []
            },
            'ioDevices': {
                'magneticTape': [],
                'printer': [],
                'hardDisk': []
            }
        }

    def set_pid(self, pid):
        self.data['pid'] = pid

    def set_processor_queues(self, lowQueue, highQueue):
        self.data['processor']['low'] = lowQueue
        self.data['processor']['high'] = highQueue

    def set_io_devices_queue(self, magneticTapeQueue, printerQueue, hardDiskQueue):
        self.data['ioDevices']['magneticTape'] = magneticTapeQueue
        self.data['ioDevices']['printer'] = printerQueue
        self.data['ioDevices']['hardDisk'] = hardDiskQueue