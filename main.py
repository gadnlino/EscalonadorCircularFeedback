import json
from configuration import Configuration

file_buffer = open("config.json")

config_json = json.load(file_buffer)

config = Configuration(**config_json)

print(len(config.processes))

for process in config.processes:
	print(process.arrivalTime)