import json
from configuration import Configuration
from scheduler import Scheduler
from models.frame import Frame
from visualization import Plotter

file_buffer = open("config.json")

config_json = json.load(file_buffer)

config = Configuration(**config_json)

scheduler = Scheduler(config)
frames = scheduler.start()

output_file_name = "output.json"

frames_json = json.dumps(list(map(lambda x : x.data, frames)))

f = open(output_file_name, "w")
f.write(frames_json)
f.close()

p = Plotter(len(config.processes))

p.plot(json.loads(frames_json))
