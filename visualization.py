from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects
from celluloid import Camera
import json
from colors import get_colors
import random


def avg(a, b):
    return (a + b) / 2.0

class Plotter:
    def __init__(self, process_count, time_slice):
        self.process_count = process_count
        self.time_slice = time_slice
        self.time = 0
        self.fig = None
        self.camera = None
        self.lines = []
        colors = get_colors()
        keys = list(colors.keys())
        random.shuffle(keys)
        self.__colors = dict([(key, colors[key]) for key in keys])

    def _plot_frame_filas(self, ax_filas, frame, i):
        def list_to_str(array):
            return map(lambda x: str(x), array)

        padding_left = 0.3
        font_size = 16

        processor_l_queue = frame['processor']['low']

        l_label = 'Fila baixa prioridade processador = [' + ','.join(list_to_str(processor_l_queue)) + ']'
        ax_filas.text(padding_left, 0.21, l_label, fontsize=font_size, transform=plt.gcf().transFigure)

        processor_h_queue = frame['processor']['high']
        h_label = 'Fila alta prioridade processador = [' + ','.join(list_to_str(processor_h_queue)) + ']'
        ax_filas.text(padding_left, 0.19, h_label, fontsize=font_size, transform=plt.gcf().transFigure)

        mag_current = frame['ioDevices']['magneticTape']['current']
        mag_current_label = 'Processo utilizando fita magnética = '

        if(mag_current != None):
            mag_current_label = mag_current_label + str(mag_current)

        ax_filas.text(padding_left, 0.17, mag_current_label, fontsize=font_size, transform=plt.gcf().transFigure)

        mag_queue = frame['ioDevices']['magneticTape']['queue']
        mag_label = 'Fila fita magnética = [' + ','.join(list_to_str(mag_queue)) + ']'
        ax_filas.text(padding_left, 0.15, mag_label, fontsize=font_size, transform=plt.gcf().transFigure)

        printer_current = frame['ioDevices']['printer']['current']
        printer_current_label = 'Processo utilizando impressora = '

        if(printer_current != None):
            printer_current_label = printer_current_label + \
                str(printer_current)

        ax_filas.text(padding_left, 0.13, printer_current_label, fontsize=font_size, transform=plt.gcf().transFigure)

        printer_queue = frame['ioDevices']['printer']['queue']
        printer_label = 'Fila impressora = [' + ','.join(list_to_str(printer_queue)) + ']'
        ax_filas.text(padding_left, 0.11, printer_label, fontsize=font_size, transform=plt.gcf().transFigure)

        hd_current = frame['ioDevices']['hardDisk']['current']
        hd_current_label = 'Processo utilizando HD = '

        if(hd_current != None):
            hd_current_label = hd_current_label + str(hd_current)

        ax_filas.text(padding_left, 0.09, hd_current_label, fontsize=font_size, transform=plt.gcf().transFigure)

        hd_queue = frame['ioDevices']['hardDisk']['queue']
        hd_label = 'Fila HD = [' + ','.join(list_to_str(hd_queue)) + ']'
        ax_filas.text(padding_left, 0.07, hd_label, fontsize=font_size, transform=plt.gcf().transFigure)

        ax_filas.text(padding_left, 0.04, f"Quantum = {self.time_slice}", fontsize=font_size, transform=plt.gcf().transFigure)
        ax_filas.text(padding_left, 0.02, f"Tempo = {i}", fontsize=font_size, transform=plt.gcf().transFigure)

    def _plot_frame_processos(self, ax_processos, frame, i):
        pid = frame["pid"]

        if(frame["pid"] != None):
            pid = frame["pid"]
        else:
            pid = -1
        # Minimizando o numero de retas a serem plotadas
        if len(self.lines) == 0:
            color = list(self.__colors.values())[pid-1]
            line = ([i-1, i], [pid, pid], color)
            self.lines.append(line)
        else:
            (xx, yy, color) = self.lines[len(self.lines) - 1]
            if yy[0] == yy[1] == pid:
                new_line = ([xx[0], i], yy, color)
                self.lines[len(self.lines) - 1] = new_line
            else:
                color = list(self.__colors.values())[pid-1]
                line = ([i-1, i], [pid, pid], color)
                self.lines.append(line)

        for xx, yy, color in self.lines:
            # t = ax_processos.plot(xx, yy, color=color,
            #                       linewidth=20.0, label=label, solid_capstyle='butt')
            #t = plt.barh(pid, xx[1] - xx[0], left=xx, color = color, edgecolor = color, align='center', height=1)
            
            #Se o processador estiver ocioso, não ploto nada
            if(yy[0] == -1):
                continue
            else:
                ax_processos.fill_between(xx, yy[0]-1, yy[0], color=color)
                txt = ax_processos.text(avg(xx[0], xx[1]), avg(yy[0]-1, yy[0]), f"{yy[0]}", 
                                        horizontalalignment='center',
                                        verticalalignment='center', color='white')
                #txt.set_path_effects([path_effects.withStroke(linewidth=2, foreground='w')])
                txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'),
                       path_effects.Normal()])

            # if(pid == -1):
            #     ax_processos.legend(t, ["Ocioso"])
            # else:
            #     ax_processos.legend(t, [f' PID {pid}'])

    def plot(self, frames, output_file="animation.gif"):
        print('Gerando gif...')

        fig, (ax_processos, ax_filas) = plt.subplots(2, 1, sharey=True, gridspec_kw={'height_ratios': [3, 1]})
        fig.set_figheight(8+(self.process_count*0.2))
        fig.set_figwidth(8+(len(frames)*0.08))
        self.fig = fig
        self.camera = Camera(self.fig)

        ax_processos.set_ylim((0, self.process_count+2))
        ax_processos.set_xlim((0, len(frames)))
        ax_processos.set_yticks(range(0, self.process_count+2, 1))

        x_spacing = 5

        if(len(frames) > 100):
            x_spacing = 10
        elif (len(frames) > 200):
            x_spacing = 20
        elif((len(frames) > 300)):
            x_spacing = 30
        elif((len(frames) > 400)):
            x_spacing = 40
        elif((len(frames) > 500)):
            x_spacing = 50

        ax_processos.set_xticks(range(0, len(frames), x_spacing))

        ax_processos.set_ylabel("PID")
        ax_processos.set_xlabel("Tempo")
        ax_processos.grid()
        ax_processos.get_yaxis().set_visible(False)

        ax_filas.axis("off")

        for i in range(0, len(frames)):
            sch_frame = frames[i-1]
            self._plot_frame_processos(ax_processos, sch_frame, i)
            self._plot_frame_filas(ax_filas, sch_frame, i)
            self.camera.snap()

        animation = self.camera.animate(interval=50)
        animation.save(output_file, dpi=100, fps=5, writer="pillow")


def test_plot():
    file_buffer = open("intermediary.json")
    frames = json.load(file_buffer)

    ptt = Plotter(4, 5)
    ptt.plot(frames)


if __name__ == "__main__":
    test_plot()
