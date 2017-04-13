from queue import Queue
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from recorder import Recorder
import audioop

class MyPlotter(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()
        self.initData()
        self.initPlotter()

    def initUI(self):
        win = pg.GraphicsWindow(title="Basic plotting examples")
        win.resize(1000, 600)
        win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # p6 = win.addPlot(title="Updating plot")
        p6 = pg.PlotWidget()
        curve = p6.plot(pen='y')
        p6.enableAutoRange('xy', True)
        self.curve = curve

        ## Create some widgets
        layout = QtGui.QGridLayout()
        label = QtGui.QLabel()
        label.setText("No input")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("QLabel { background-color : white; color : black; }")
        layout.addWidget(label, 1, 0)
        layout.addWidget(p6, 0, 0)

        self.setLayout(layout)
        self.resize(1000, 600)
        self.setWindowTitle('LiveFFT')
        self.show()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.handleNewData)
        timer.start(100)
        # keep reference to timer
        self.timer = timer

    def initData(self):
        rec = Recorder()
        rec.start()
        self.rec = rec
        self.rms = 0.0#audioop.rms(rec.frames[0],2)

    def initPlotter(self):
        pass

    def handleNewData(self):
        frames = self.rec.get_frames()
        if len(frames) > 0:
            current_frame = frames[-1]
            self.curve.setData(current_frame)


# TODO Move to main.py
# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        # QtGui.QApplication.instance().exec_()
        app = QtGui.QApplication(sys.argv)
        window = MyPlotter()
        sys.exit(app.exec_())
