import json
from configuration import Configuration
from scheduler import Scheduler
from models.frame import Frame

file_buffer = open("config.json")

config_json = json.load(file_buffer)

config = Configuration(**config_json)

# print(len(config.processes))
# print("-------------------------")
# for process in config.processes:
# 	print(process.arrivalTime)
# 	for inte in process.interruptions:
# 		print("category={}, time = {}".format(inte.category, inte.time))
# 	print("||||||")

#print(json.dumps([Frame().data]))

scheduler = Scheduler(config)
#print(vars(config))
scheduler.start()
