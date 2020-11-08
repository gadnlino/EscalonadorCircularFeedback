from matplotlib import pyplot as plt
from celluloid import Camera
import json
from colors import get_colors
import random


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
            return map(lambda x : str(x), array)

        padding_left = 0.3
        font_size = 16        

        processor_l_queue = frame['processor']['low']

        l_label = 'Fila baixa prioridade processador = [' + ','.join(list_to_str(processor_l_queue)) + ']'
        ax_filas.text(padding_left, 3.6, l_label, fontsize=font_size)

        processor_h_queue = frame['processor']['high']
        h_label = 'Fila alta prioridade processador = [' + ','.join(list_to_str(processor_h_queue)) + ']'
        ax_filas.text(padding_left, 3.3, h_label, fontsize=font_size)

        mag_current = frame['ioDevices']['magneticTape']['current']
        mag_current_label = 'Processo utilizando fita magnética = '
        
        if(mag_current != None):
            mag_current_label = mag_current_label + str(mag_current)

        ax_filas.text(padding_left, 3.0, mag_current_label, fontsize=font_size)

        mag_queue = frame['ioDevices']['magneticTape']['queue']
        mag_label = 'Fila fita magnética = [' + ','.join(list_to_str(mag_queue)) + ']'
        ax_filas.text(padding_left, 2.7, mag_label, fontsize=font_size)

        printer_current = frame['ioDevices']['printer']['current']
        printer_current_label = 'Processo utilizando impressora = '
        
        if(printer_current != None):
            printer_current_label = printer_current_label + str(printer_current)

        ax_filas.text(padding_left, 2.4, printer_current_label, fontsize=font_size)

        printer_queue = frame['ioDevices']['printer']['queue']
        printer_label = 'Fila impressora = [' + ','.join(list_to_str(printer_queue)) + ']'
        ax_filas.text(padding_left, 2.1, printer_label, fontsize=font_size)

        hd_current = frame['ioDevices']['hardDisk']['current']
        hd_current_label = 'Processo utilizando HD = '
        
        if(hd_current != None):
            hd_current_label = hd_current_label + str(hd_current)

        ax_filas.text(padding_left, 1.8, hd_current_label, fontsize=font_size)

        hd_queue = frame['ioDevices']['hardDisk']['queue']
        hd_label = 'Fila HD = [' + ','.join(list_to_str(hd_queue)) + ']'
        ax_filas.text(padding_left, 1.5, hd_label, fontsize=font_size)

        ax_filas.text(padding_left, 0.75, f"Quantum = {self.time_slice}", fontsize=font_size)
        ax_filas.text(padding_left, 0.4, f"Tempo = {i}", fontsize=font_size)

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

        label = "PID {}".format(pid) if pid != -1 else "Ocioso"
        for xx, yy, color in self.lines:
            t = ax_processos.plot(xx, yy, color=color,
                                  linewidth=4.0, label=label)

            if(pid == -1):
                ax_processos.legend(t, ["Ocioso"])
            else:
                ax_processos.legend(t, [f' PID {pid}'])

    def plot(self, frames, output_file="animation.gif"):
        fig, (ax_processos, ax_filas) = plt.subplots(2, 1, sharey=True)
        fig.set_figheight(8)
        fig.set_figwidth(12)
        self.fig = fig
        self.camera = Camera(self.fig)

        ax_processos.set_ylim((0, self.process_count+2))
        ax_processos.set_xlim((0, len(frames)))
        ax_processos.set_yticks(range(0, self.process_count+2, 1))
        ax_processos.set_xticks(range(0, len(frames), 5))

        ax_processos.set_ylabel("PID")
        ax_processos.set_xlabel("Tempo")
        ax_processos.grid()

        ax_filas.axis("off")

        for i in range(0, len(frames)):
            sch_frame = frames[i-1]
            self._plot_frame_processos(ax_processos, sch_frame, i)
            self._plot_frame_filas(ax_filas, sch_frame, i)
            self.camera.snap()

        animation = self.camera.animate(interval=50)
        animation.save(output_file, dpi=100, fps=5)

def test_plot():
    file_buffer = open("intermediary.json")
    frames = json.load(file_buffer)

    ptt = Plotter(4, 5)
    ptt.plot(frames)

if __name__ == "__main__":
    test_plot()
