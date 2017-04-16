from collections import deque
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph
from recorder import Recorder
import audioop


# Plots sound graph from microphone
class Plotter(QtGui.QWidget):
    RMS_QUEUE_SIZE = 100  # RMS queue size in timer intervals
    TIMER_INTERVAL = 100  # Timer interval in milliseconds

    def __init__(self, width, height):
        QtGui.QWidget.__init__(self)

        # Initialize the recorder
        recorder = Recorder()
        recorder.start()
        self.recorder = recorder
        self.rms_deque = deque(maxlen=Plotter.RMS_QUEUE_SIZE)

        # Initialize the user interface
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        self.resize(width, height)
        self.setWindowTitle('PyAudio Demo')

        # Create plots
        pyqtgraph.setConfigOptions(antialias=True)
        oscilloscope_widget = pyqtgraph.PlotWidget()
        oscilloscope_curve = oscilloscope_widget.plot(pen='y')
        oscilloscope_widget.enableAutoRange('x', True)  # TODO Extract constants when measurement units are identified
        oscilloscope_widget.setYRange(-50000,50000)
        self.oscilloscope_curve = oscilloscope_curve

        volume_widget = pyqtgraph.PlotWidget()
        volume_curve = volume_widget.plot(pen='y')
        volume_widget.setYRange(0, 16000)
        volume_widget.setXRange(0, Plotter.RMS_QUEUE_SIZE)
        self.volume_curve = volume_curve

        # Create other widgets
        layout.addWidget(oscilloscope_widget, 0, 0)
        layout.addWidget(volume_widget,0, 1)

        self.show()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.handle_new_data)
        timer.start(Plotter.TIMER_INTERVAL)
        self.timer = timer


    # Handle callback data from recorder
    def handle_new_data(self):
        frames = self.recorder.get_frames()
        if len(frames) > 0:
            current_frame = frames[-1]
            rms = audioop.rms(current_frame,2)
            self.rms_deque.append(rms)
            self.oscilloscope_curve.setData(current_frame)
            self.volume_curve.setData(list(self.rms_deque))


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication(sys.argv)
        screen_rect = app.desktop().screenGeometry()
        window = Plotter(screen_rect.width(), screen_rect.height())
        sys.exit(app.exec_())
