from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from helperclasses.constants import Constants

class Filter(QWidget):

    def __init__(self, connectFunction):
        super(Filter, self).__init__()

        self.filter_cb = QComboBox()
        self.filter_cb.addItems(["All", Constants.DISTANCES[0], Constants.DISTANCES[1], Constants.DISTANCES[2], 
            Constants.DISTANCES[3], Constants.DISTANCES[4], Constants.DISTANCES[5]])
        self.filter_cb.setFixedWidth(150)
        self.filter_cb.currentIndexChanged.connect(connectFunction)

        self.filter_lyt = QHBoxLayout()
        self.filter_lyt.addWidget(QLabel("Show "))
        self.filter_lyt.addWidget(self.filter_cb)
        self.filter_lyt.addStretch()
    
    def filter_distance(self, filter):
        if filter == self.filter_cb.itemText(0):
            return filter
        elif filter == self.filter_cb.itemText(1):
            return 5
        elif filter == self.filter_cb.itemText(2):
            return 10
        elif filter == self.filter_cb.itemText(3):
            return 15
        elif filter == self.filter_cb.itemText(4):
            return 21
        elif filter == self.filter_cb.itemText(5):
            return 30
        elif filter == self.filter_cb.itemText(6):
            return 42
    