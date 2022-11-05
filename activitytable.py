from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from constants import Constants


class ActivityTable(QWidget):

    def __init__(self, activities, latest_activity):
        super(ActivityTable, self).__init__()

        # Table Layout
        table_lyt = QGridLayout()
        table_lyt.setHorizontalSpacing(0)

        # Horizontal Headers
        for d in range(len(Constants.DATA_TYPES)):
            label = QLabel(Constants.DATA_TYPES[d] + Constants.DATA_UNITS[d])
            label.setStyleSheet('''font-weight: bold;''')
            table_lyt.addWidget(label, 0, d)

        

        # Add Activities
        row = 1
        for a in activities:
            a1 = QLabel(str(a[1]))
            a2 = QLabel(str(a[2]))
            a3 = QLabel(str(a[3]))
            a4 = QLabel(str(a[4]))
            a5 = QLabel(str(a[5]))
            a6 = QLabel(str(a[6]))

            if a[0] == latest_activity[0]:
                background_color = "yellow"
                a1.setStyleSheet(f"background-color : {background_color}")
                a2.setStyleSheet("background-color : yellow")
                a3.setStyleSheet("background-color : yellow")
                a4.setStyleSheet("background-color : yellow")
                a5.setStyleSheet("background-color : yellow")
                a6.setStyleSheet("background-color : yellow")

            table_lyt.addWidget(a1, row, 0)
            table_lyt.addWidget(a2, row, 1)
            table_lyt.addWidget(a3, row, 2)
            table_lyt.addWidget(a4, row, 3)
            table_lyt.addWidget(a5, row, 4)
            table_lyt.addWidget(a6, row, 5)
            row=row+1

        lay2 = QVBoxLayout()
        lay2.addLayout(table_lyt)
        lay2.addStretch()
        
        # Main Layout
        table = QWidget()
        table.setLayout(lay2)


        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(table)
        #scroll.setFixedHeight(500)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        
        
        # Main Layout
        main_lyt = QVBoxLayout()
        main_lyt.addWidget(scroll)
        self.setLayout(main_lyt)
