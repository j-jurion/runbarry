from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from helperclasses.constants import Constants

class Sorter(QWidget):

    def __init__(self, connectFunction):
        super(Sorter, self).__init__()

        self.asc = "\u25BC"
        self.desc ="\u25B2"

        self.sorter_cb = QComboBox()
        self.sorter_cb.addItems([Constants.DATA_TYPES[0], Constants.DATA_TYPES[1], Constants.DATA_TYPES[2], Constants.DATA_TYPES[3], Constants.DATA_TYPES[4], Constants.DATA_TYPES[5]])
        self.sorter_cb.setFixedWidth(70)
        self.sorter_cb.setCurrentIndex(1)
        self.sorter_cb.currentIndexChanged.connect(connectFunction)

        self.order_btn = QPushButton(self.desc)
        self.order_btn.setFixedWidth(30)
        self.order_btn.clicked.connect(lambda:self.order_toggle(connectFunction))

        self.sorter_lyt = QHBoxLayout()
        self.sorter_lyt.addWidget(QLabel("Sort by "))
        self.sorter_lyt.addWidget(self.sorter_cb)
        self.sorter_lyt.addWidget(self.order_btn)
        self.sorter_lyt.addStretch()
    
    def order_toggle(self, connectFunction):
        if self.order_btn.text() == self.asc:
            self.order_btn.setText(self.desc)
        else:
            self.order_btn.setText(self.asc)
        connectFunction()

    def order_btn_string(self):
        if self.order_btn.text() == self.asc:
            return "ASC"
        else: return "DESC"
    