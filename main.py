import json
from configuration import Configuration
from scheduler import Scheduler
from models.frame import Frame
from visualization import Plotter
import sys
import argparse

def main():
	inputfile = ''
	outputfile = ''
	parser = argparse.ArgumentParser(description="A processor scheduler simulator, implementing the round robin and feedback policy.")
	parser.add_argument('--input_file', help='The name of the input configuration file.')
	parser.add_argument('--output_file', help='The name of the output file.')
	args = parser.parse_args()
	args_dict = vars(args)

	if(not args_dict["input_file"] != None and
		 not args_dict["output_file"] != None):
		parser.print_help()
		sys.exit(1)

	inputfile = args_dict["input_file"]
	outputfile = args_dict["output_file"]

	file_buffer = open(inputfile)
	config_json = json.load(file_buffer)
	config = Configuration(**config_json)
	scheduler = Scheduler(config)
	frames = scheduler.start()
	intermediary_file = "intermediary.json"
	frames_json = json.dumps(list(map(lambda x: x.data, frames)))
	f = open(intermediary_file, "w")
	f.write(frames_json)
	f.close()
	p = Plotter(len(config.processes))
	p.plot(json.loads(frames_json), output_file=outputfile)

if __name__ == "__main__":
    main()
