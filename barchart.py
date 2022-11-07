from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class BarChart(FigureCanvasQTAgg):

    def __init__(self, database):
        fig = Figure(figsize=(5, 10), dpi=100)
        self.axes = fig.add_subplot(111)

        super(BarChart, self).__init__(fig)
        
        x = []
        y = []
        for m in database.get_months():
            x.append(m[1])
            y.append(m[2])

        self.axes.bar(x, y, width=0.8, color='lightblue')
        self.axes.set_xticklabels(x, rotation=45)
        plt.xticks(rotation = 45)
