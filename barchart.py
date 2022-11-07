from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from constants import Constants

class BarChartWidget(QWidget):

    def __init__(self, database):
        super(BarChartWidget, self).__init__()
        layout = QVBoxLayout()
        chart = BarChart(database)
        layout.addWidget(chart)
        layout.addStretch()

        lyt = QVBoxLayout()
        group_box = QGroupBox("Graph Total Distance")
        group_box.setLayout(layout)
        lyt.addWidget(group_box)
        self.setLayout(lyt)


class BarChart(FigureCanvasQTAgg):

    def __init__(self, database):
        fig = Figure(figsize=(5, 10), dpi=100)
        self.axes = fig.add_subplot(111)
        #fig.subplots_adjust(bottom=0, top=1)

        super(BarChart, self).__init__(fig)
        
        x = []
        y = []
        for m in reversed(database.get_months()):
            x.append(m[1])
            y.append(m[2])

        self.axes.bar(x, y, width=0.8, color=Constants.COLOR_PRIM)

        #elf.axes.set_xticklabels(x, rotation=45)
        #plt.xticks(rotation = 45)
