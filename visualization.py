from matplotlib import pyplot as plt
from celluloid import Camera
import json
from colors import get_colors
import random


class Plotter:
    def __init__(self, process_count):
        self.process_count = process_count
        self.time = 0
        self.fig = None
        self.camera = None
        self.lines = []
        colors = get_colors()
        keys = list(colors.keys())
        random.shuffle(keys)
        self.__colors = dict([(key, colors[key]) for key in keys])

    def _make_line(self, x1, x2, y1, y2):
        steps = 100
        dx = (x2-x1)/steps
        dy = (y2-y1) / steps

        xs = []
        ys = []

        for i in range(steps+1):
            xs.append(x1 + dx * i)
            ys.append(y1 + dy * i)

        return xs, ys

    def plot(self, frames, output_file="animation.gif"):
        self.fig = plt.figure()
        self.camera = Camera(self.fig)
        ax = plt.axes()
        ax.set_ylim((0, self.process_count+1))
        ax.set_xlim((0, len(frames)))

        ax.set_xlabel("Tempo")
        ax.set_ylabel("PID")

        for i in range(len(frames)):
            sch_frame = frames[i]

            pid = sch_frame["pid"]

            xs, ys = self._make_line(i, i+1, pid, pid)
            color = list(self.__colors.values())[pid-1]

            self.lines.append((xs, ys, color))

            for xx, yy, color in self.lines:
                t = ax.plot(xx, yy, color=color)

            plt.legend(t, [f' PID {pid}'])
            self.camera.snap()
        animation = self.camera.animate()
        animation.save(output_file)


def test_plot():
    file_buffer = open("output.json")
    frames = json.load(file_buffer)

    ptt = Plotter(4)
    ptt.plot(frames)


if __name__ == "__main__":
    test_plot()
