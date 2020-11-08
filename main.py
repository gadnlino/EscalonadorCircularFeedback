import json
from configuration import Configuration
from scheduler import Scheduler
from models.frame import Frame
from visualization import Plotter
import sys
import argparse


def main():
    inputfile = ''
    parser = argparse.ArgumentParser(
        description="A processor scheduler simulator, implementing the round robin and feedback policy.")
    parser.add_argument(
        '-i', '--input-file', help='The name of the input configuration file.')
    parser.add_argument('--output-type', help='The type of the output file.',
                        choices=['gif', 'stdout'], default='stdout')
    parser.add_argument('--save-intermediary', action='store_true')
    args = parser.parse_args()
    args_dict = vars(args)

    if(args_dict["input_file"] == None):
        parser.print_help()
        sys.exit(1)

    inputfile = args_dict["input_file"]

    file_buffer = open(inputfile)
    config_json = json.load(file_buffer)
    config = Configuration(**config_json)
    scheduler = Scheduler(config)
    frames = scheduler.start()

    frames_json = json.dumps(list(map(lambda x: x.data, frames)))

    if(args_dict['save_intermediary'] == True):
        intermediary_file = "intermediary.json"
        f = open(intermediary_file, "w")
        f.write(frames_json)
        f.close()

    if(args_dict['output_type'] == 'gif'):
        p = Plotter(len(config.processes), config.timeSlice)
        p.plot(json.loads(frames_json))

if __name__ == "__main__":
    main()
