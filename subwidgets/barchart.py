from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from helperclasses.constants import Constants

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

        super(BarChart, self).__init__(fig)
        
        x = []
        y = []
        for m in reversed(database.get_months()):
            x.append(m[1])
            y.append(m[2])

        self.axes.bar(x, y, width=0.8, color=Constants.COLOR_PRIM)

        self.axes.set_xticks(self.axes.get_xticks())
        self.axes.set_xticklabels(x, rotation=90)

        fig.subplots_adjust(bottom=0.25, top=0.95)
