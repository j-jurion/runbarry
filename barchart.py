from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg

class BarChart(QWidget):

    def __init__(self, database):
        super(BarChart, self).__init__()

        self.database = database

        layout = QVBoxLayout()

        plot = pg.plot()
 
        x = []
        y = []
        for m in self.database.get_months():
            x.append(m[1])
            y.append(m[2])

        print(x)
        print(y)
        x = [1, 2]
 
        bargraph = pg.BarGraphItem(x = x, height = y, width = 0.6, brush ='b')
 
        plot.addItem(bargraph)

        layout.addWidget(plot)
        layout.addStretch()
        self.setLayout(layout)